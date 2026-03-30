"""ClawHub飞书智能体框架 - 主应用程序"""
import uvicorn
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import os
from dotenv import load_dotenv

from src.feishu.client import FeishuClient, FeishuConfig
from src.agents.feishu_agent import FeishuAgent
from src.core.agent import AgentConfig
from src.plugins.message_processor import MessageProcessorPlugin
from src.core.plugin import PluginManager, PluginConfig

# 加载环境变量
load_dotenv()

# 配置日志
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(os.getenv("LOG_FILE", "./logs/clawhub.log")),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 创建FastAPI应用
app = FastAPI(
    title="ClawHub智能体框架",
    description="基于插件的智能体开发框架，支持飞书集成",
    version="2.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局变量
feishu_agent = None

@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    global feishu_agent
    
    logger.info("正在启动ClawHub智能体框架...")
    
    # 初始化飞书配置
    feishu_config = FeishuConfig(
        app_id=os.getenv("FEISHU_APP_ID", ""),
        app_secret=os.getenv("FEISHU_APP_SECRET", ""),
        verification_token=os.getenv("FEISHU_VERIFICATION_TOKEN", ""),
        encrypt_key=os.getenv("FEISHU_ENCRYPT_KEY") or None
    )
    
    # 验证配置
    if not feishu_config.app_id or not feishu_config.app_secret:
        logger.warning("飞书配置不完整，智能体功能可能受限")
    
    # 创建智能体配置
    agent_config = AgentConfig(
        name="ClawHub智能体",
        description="基于插件系统的智能体框架，支持飞书集成",
        skills=["message_processing", "context_management", "memory_management"],
        plugins=["message_processor", "workflow_engine", "skill_library"],
        memory_size=200,
        max_context_length=20,
        enable_history=True,
        enable_learning=True,
        response_timeout=30,
        config={
            "debug": os.getenv("DEBUG", "false").lower() == "true",
            "log_level": os.getenv("LOG_LEVEL", "INFO"),
        }
    )
    
    # 创建飞书智能体
    feishu_agent = FeishuAgent(agent_config, feishu_config)
    
    # 初始化插件管理器
    plugin_manager = PluginManager()
    
    # 注册消息处理器插件
    message_processor_config = PluginConfig(
        name="message_processor",
        enabled=True,
        priority=80,
        config={
            "sensitive_patterns": [
                r"password.*",
                r"token.*",
                r"secret.*",
                r"密钥.*",
                r"密码.*",
            ],
            "enable_intent_detection": True,
            "enable_sentiment_analysis": True,
            "max_length": 2000,
        }
    )
    
    message_processor = MessageProcessorPlugin()
    plugin_manager.register_plugin(message_processor, message_processor_config)
    
    # 将插件管理器设置给智能体
    feishu_agent.plugin_manager = plugin_manager
    
    # 初始化智能体
    await feishu_agent.initialize()
    
    logger.info("ClawHub智能体框架启动完成")
    logger.info(f"智能体名称: {feishu_agent.name}")
    logger.info(f"插件数量: {len(plugin_manager.plugins)}")
    logger.info(f"记忆容量: {agent_config.memory_size}")

@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时清理"""
    global feishu_agent
    if feishu_agent:
        # 关闭智能体
        await feishu_agent.shutdown()
        
        # 关闭插件管理器
        if hasattr(feishu_agent, 'plugin_manager'):
            await feishu_agent.plugin_manager.shutdown_all()
            
    logger.info("ClawHub智能体框架已关闭")

@app.get("/")
async def root():
    """根路径"""
    global feishu_agent
    
    agent_status = {}
    if feishu_agent:
        agent_status = feishu_agent.get_detailed_status()
    
    return {
        "service": "ClawHub智能体框架",
        "version": "2.0.0",
        "status": "running",
        "agent": agent_status.get("name", "未初始化"),
        "agent_status": "运行中" if feishu_agent else "未初始化",
        "endpoints": {
            "health": "/health",
            "status": "/api/status",
            "webhook": "/webhook/feishu",
            "test_message": "/api/send-test",
            "plugins": "/api/plugins",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
async def health_check():
    """健康检查"""
    global feishu_agent
    
    from datetime import datetime
    
    status = "healthy"
    
    if not feishu_agent:
        status = "warning: agent not initialized"
    elif hasattr(feishu_agent, 'stats') and feishu_agent.stats.get("errors", 0) > 10:
        status = "warning: high error rate"
    
    return {
        "status": status,
        "timestamp": datetime.now().isoformat() + "Z",
        "agent_initialized": bool(feishu_agent),
        "uptime": feishu_agent.stats.get("uptime", 0) if feishu_agent else 0,
    }

@app.post("/webhook/feishu")
async def feishu_webhook(request: Request, background_tasks: BackgroundTasks):
    """飞书Webhook回调接口"""
    global feishu_agent
    
    if not feishu_agent:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    try:
        # 获取请求头
        signature = request.headers.get("X-Lark-Signature", "")
        timestamp = request.headers.get("X-Lark-Request-Timestamp", "")
        nonce = request.headers.get("X-Lark-Request-Nonce", "")
        
        # 获取请求体
        body = await request.body()
        body_str = body.decode("utf-8")
        
        # 使用智能体的Webhook处理
        result = await feishu_agent.handle_feishu_webhook(
            signature=signature,
            timestamp=timestamp,
            nonce=nonce,
            encrypted_message=body_str,
        )
        
        # 如果是URL验证，直接返回challenge
        if "challenge" in result:
            return JSONResponse(content=result)
        
        # 其他事件返回处理成功
        return {"status": "processed", "agent": feishu_agent.name}
        
    except Exception as e:
        logger.error(f"处理飞书Webhook失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def get_agent_status():
    """获取智能体状态"""
    global feishu_agent
    
    if not feishu_agent:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    try:
        agent_status = feishu_agent.get_detailed_status()
        feishu_status = feishu_agent.get_feishu_status()
        
        return {
            "agent": agent_status,
            "feishu": feishu_status,
            "plugins": feishu_agent.plugin_manager.list_plugins() if hasattr(feishu_agent, 'plugin_manager') else [],
            "system": {
                "python_version": os.sys.version,
                "platform": os.sys.platform,
                "working_directory": os.getcwd(),
            }
        }
    except Exception as e:
        logger.error(f"获取智能体状态失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/plugins")
async def get_plugins():
    """获取插件列表"""
    global feishu_agent
    
    if not feishu_agent:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    if not hasattr(feishu_agent, 'plugin_manager'):
        return {"plugins": [], "message": "插件管理器未初始化"}
    
    plugins = feishu_agent.plugin_manager.list_plugins()
    pipeline = feishu_agent.plugin_manager.get_pipeline_order()
    
    return {
        "total_plugins": len(plugins),
        "enabled_plugins": len(pipeline),
        "plugins": plugins,
        "pipeline_order": pipeline,
    }

@app.get("/api/send-test")
async def send_test_message(user_id: str = "ou_1234567890", message: str = None):
    """发送测试消息（开发用）"""
    global feishu_agent
    
    if not feishu_agent:
        raise HTTPException(status_code=503, detail="智能体未初始化")
    
    try:
        test_message = message or "这是一条来自ClawHub智能体框架的测试消息！"
        success = await feishu_agent.send_test_message(user_id, test_message)
        
        if success:
            return {
                "status": "success",
                "message": "测试消息已发送",
                "agent": feishu_agent.name,
                "recipient": user_id,
                "content": test_message,
            }
        else:
            raise HTTPException(status_code=500, detail="发送测试消息失败")
            
    except Exception as e:
        logger.error(f"发送测试消息失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("SERVER_HOST", "0.0.0.0")
    port = int(os.getenv("SERVER_PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    logger.info(f"启动ClawHub智能体框架服务器: {host}:{port}")
    logger.info(f"调试模式: {debug}")
    logger.info(f"Python版本: {os.sys.version}")
    logger.info(f"工作目录: {os.getcwd()}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info"
    )