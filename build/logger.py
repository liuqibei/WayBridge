import logging
import colorlog
import sys
from typing import Optional


class Logger:
    _logger: Optional[logging.Logger] = None
    _initialized: bool = False

    @staticmethod
    def _setup_logger() -> logging.Logger:
        """设置并返回配置好的logger实例"""
        if Logger._logger is not None:
            return Logger._logger

        # 创建logger
        logger = logging.getLogger("BUILD")
        logger.setLevel(logging.DEBUG)

        # 避免重复添加处理器
        if logger.handlers:
            return logger

        # 创建控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # 创建彩色格式器
        color_formatter = colorlog.ColoredFormatter(
            fmt="%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            },
        )

        console_handler.setFormatter(color_formatter)
        logger.addHandler(console_handler)

        # 禁止传播到根logger，避免重复输出
        logger.propagate = False

        Logger._logger = logger
        Logger._initialized = True
        return logger

    @staticmethod
    def debug(message: str) -> None:
        """记录DEBUG级别日志"""
        logger = Logger._setup_logger()
        logger.debug(message)

    @staticmethod
    def info(message: str) -> None:
        """记录INFO级别日志"""
        logger = Logger._setup_logger()
        logger.info(message)

    @staticmethod
    def warning(message: str) -> None:
        """记录WARNING级别日志"""
        logger = Logger._setup_logger()
        logger.warning(message)

    @staticmethod
    def error(message: str) -> None:
        """记录ERROR级别日志"""
        logger = Logger._setup_logger()
        logger.error(message)

    @staticmethod
    def critical(message: str) -> None:
        """记录CRITICAL级别日志"""
        logger = Logger._setup_logger()
        logger.critical(message)

    @staticmethod
    def set_level(level: int) -> None:
        """设置日志级别"""
        logger = Logger._setup_logger()
        logger.setLevel(level)

    @staticmethod
    def get_logger() -> logging.Logger:
        """获取底层logger实例（用于高级用法）"""
        return Logger._setup_logger()
