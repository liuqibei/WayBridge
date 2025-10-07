from logger import Logger
import subprocess
from typing import List, Union
import argparse
import os


def execute_process(process_name: str, args: Union[List[str], str]) -> bool:
    """
    执行一个外部进程，并将stdout和stderr分别重定向到日志的info和error级别

    Args:
        process_name: 进程名称（用于日志标识）
        args: 进程参数，可以是字符串或字符串列表

    Returns:
        bool: True表示进程正常退出（返回码为0），False表示异常退出
    """
    # 标准化参数格式
    if isinstance(args, str):
        cmd = args.split()
    else:
        cmd = args

    if not cmd:
        Logger.error(f"[{process_name}] 命令参数为空")
        return False

    # 如果第一个参数不是进程名称，将进程名称添加到命令开头
    if cmd[0] != process_name:
        cmd = [process_name] + cmd

    try:
        Logger.info(f"[{process_name}] 开始执行命令: {' '.join(cmd)}")

        # 执行进程，捕获stdout和stderr
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,  # 以文本模式处理输出
            encoding="utf-8",  # 指定编码
            bufsize=1,  # 行缓冲
        )

        # 实时读取stdout并记录到info日志
        if process.stdout:
            for line in iter(process.stdout.readline, ""):
                line = line.rstrip("\n\r")
                if line:  # 忽略空行
                    Logger.info(f"[{process_name}] {line}")
            process.stdout.close()

        # 读取stderr并记录到error日志
        stderr_output = []
        if process.stderr:
            for line in iter(process.stderr.readline, ""):
                line = line.rstrip("\n\r")
                if line:  # 忽略空行
                    Logger.error(f"[{process_name}] {line}")
                    stderr_output.append(line)
            process.stderr.close()

        # 等待进程结束
        return_code = process.wait()

        if return_code == 0:
            Logger.info(f"[{process_name}] 进程正常退出 (返回码: {return_code})")
            return True
        else:
            Logger.error(f"[{process_name}] 进程异常退出 (返回码: {return_code})")
            return False

    except FileNotFoundError:
        Logger.error(f"[{process_name}] 找不到可执行文件: {cmd[0]}")
        return False
    except PermissionError:
        Logger.error(f"[{process_name}] 没有执行权限: {cmd[0]}")
        return False
    except subprocess.SubprocessError as e:
        Logger.error(f"[{process_name}] 进程执行错误: {str(e)}")
        return False
    except Exception as e:
        Logger.error(f"[{process_name}] 未知错误: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Welcome to WayBridge")
    parser.add_argument(
        "-t", "--type", type=str, help="Build Type (Debug|Release)", default="Release"
    )
    parser.add_argument("-d", "--build-dir", help="Build Dir", default="out")
    args = parser.parse_args()

    execute_process(
        "cmake",
        [
            f"-B{args.build_dir}",
            f"-GNinja",
            f"-S{os.getcwd()}",
            f"-DCMAKE_BUILD_TYPE={args.type}",
        ],
    )

    execute_process("cmake", [f"--build", args.build_dir])


if __name__ == "__main__":
    main()
