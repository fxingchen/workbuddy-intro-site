"""应用配置管理"""
import os
from typing import Optional
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    """应用配置"""
    
    # 飞书配置
    feishu_app_id: str = os.getenv("FEISHU_APP_ID", "")
    feishu_app_secret: str = os.getenv("FEISHU_APP_SECRET", "")
    feishu_verification_token: str = os.getenv("FEISHU_VERIFICATION_TOKEN", "")
    feishu_encrypt_key: Optional[str] = os.getenv("FEISHU_ENCRYPT_KEY")
    
    # 服务器配置
    server_host: str = os.getenv("SERVER_HOST", "0.0.0.0")
    server_port: int = int(os.getenv("SERVER_PORT", "8000"))
    debug: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # 数据库配置
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./claw.db")
    
    # Redis配置
    redis_url: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # 安全配置
    secret_key: str = os.getenv("SECRET_KEY", "your_secret_key_here_change_this_in_production")
    allowed_hosts: list = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    
    # 日志配置
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    log_file: str = os.getenv("LOG_FILE", "./logs/claw.log")
    
    class Config:
        env_file = ".env"
        
    def validate_feishu_config(self) -> bool:
        """验证飞书配置是否完整"""
        return all([
            self.feishu_app_id,
            self.feishu_app_secret,
            self.feishu_verification_token
        ])

# 全局配置实例
settings = Settings()