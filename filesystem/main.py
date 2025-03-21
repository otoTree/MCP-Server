from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
import os
import shutil
import aiofiles
import asyncio
from pathlib import Path
from typing import Union, List
import csv
from typing import Union
from docx import Document
import pandas as pd
import json
import xml.etree.ElementTree as ET

mcp = FastMCP("filesystem")


@mcp.tool()
async def create_file(file_path: str, content: str = "") -> bool:
    """
    创建新文件并写入内容，返回是否成功。

    Args:
        file_path (str): 文件的完整路径，包括文件名和扩展名。
        content (str, optional): 要写入文件的内容。如果未提供，则创建空文件。

    Returns:
        bool: 文件创建是否成功。
    """
    try:
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(content)
        return True
    except Exception as e:
        print(f"创建文件失败: {e}")
        return False

@mcp.tool()
async def save_file(file_path: str, content: str, file_format: str = "txt") -> bool:
    """
    保存文件，支持指定格式，返回是否成功。

    Args:
        file_path (str): 文件路径，可以包含或不包含扩展名。
        content (str): 要写入文件的内容。
        file_format (str, optional): 文件的扩展名，默认为 "txt"。

    Returns:
        bool: 文件保存是否成功。
    """
    try:
        if not file_path.endswith(f".{file_format}"):
            file_path = f"{file_path}.{file_format}"
        async with aiofiles.open(file_path, mode='w') as f:
            await f.write(content)
        return True
    except Exception as e:
        print(f"保存文件失败: {e}")
        return False

@mcp.tool()
async def copy_file(src: str, dst: str) -> bool:
    """
    复制单个文件，返回是否成功。

    Args:
        src (str): 源文件的路径。
        dst (str): 目标文件的路径。

    Returns:
        bool: 文件复制是否成功。
    """
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"复制文件失败: {e}")
        return False

@mcp.tool()
async def move_file(src: str, dst: str) -> bool:
    """
    移动单个文件，返回是否成功。

    Args:
        src (str): 源文件的路径。
        dst (str): 目标文件的路径。

    Returns:
        bool: 文件移动是否成功。
    """
    try:
        shutil.move(src, dst)
        return True
    except Exception as e:
        print(f"移动文件失败: {e}")
        return False
    
@mcp.tool() 
async def batch_copy_files(src_paths: List[str], dst_dir: str) -> List[bool]:
    """
    批量复制文件，返回每个文件复制是否成功。

    Args:
        src_paths (List[str]): 源文件路径列表。
        dst_dir (str): 目标文件夹路径。

    Returns:
        List[bool]: 每个文件复制的成功状态列表。
    """
    results = []
    for src in src_paths:
        dst = os.path.join(dst_dir, os.path.basename(src))
        success = await copy_file(src, dst)
        results.append(success)
    return results

@mcp.tool()
async def batch_move_files(src_paths: List[str], dst_dir: str) -> List[bool]:
    """
    批量移动文件，返回每个文件移动是否成功。

    Args:
        src_paths (List[str]): 源文件路径列表。
        dst_dir (str): 目标文件夹路径。

    Returns:
        List[bool]: 每个文件移动的成功状态列表。
    """
    results = []
    for src in src_paths:
        dst = os.path.join(dst_dir, os.path.basename(src))
        success = await move_file(src, dst)
        results.append(success)
    return results

@mcp.tool()
async def delete_file(file_path: str, permanent: bool = False) -> bool:
    """
    删除文件，可选择彻底删除，返回是否成功。

    Args:
        file_path (str): 要删除的文件路径。
        permanent (bool, optional): 是否永久删除，默认为 False。

    Returns:
        bool: 文件删除是否成功。
    """
    try:
        if permanent:
            os.unlink(file_path)
        else:
            os.remove(file_path)
        return True
    except Exception as e:
        print(f"删除文件失败: {e}")
        return False

@mcp.tool()
async def restore_file_from_recycle_bin(file_path: str) -> bool:
    """
    模拟从回收站恢复文件，返回是否成功。

    Args:
        file_path (str): 要恢复的文件路径。

    Returns:
        bool: 文件恢复是否成功。
    """
    try:
        Path(file_path).touch()  # 模拟恢复文件
        return True
    except Exception as e:
        print(f"恢复文件失败: {e}")
        return False

@mcp.tool()
async def search_files(directory: str, keyword: str) -> List[str]:
    """
    搜索指定目录下的文件，返回匹配的文件路径列表。

    Args:
        directory (str): 要搜索的目录路径。
        keyword (str): 搜索关键词。

    Returns:
        List[str]: 匹配的文件路径列表。
    """
    try:
        return [os.path.join(root, file) for root, _, files in os.walk(directory) for file in files if keyword in file]
    except Exception as e:
        print(f"搜索文件失败: {e}")
        return []

@mcp.tool()
async def create_folder(folder_path: str) -> bool:
    """
    创建文件夹，返回是否成功。

    Args:
        folder_path (str): 要创建的文件夹路径。

    Returns:
        bool: 文件夹创建是否成功。
    """
    try:
        os.makedirs(folder_path, exist_ok=True)
        return True
    except Exception as e:
        print(f"创建文件夹失败: {e}")
        return False

@mcp.tool()
async def compress_folder(src_dir: str, dst_zip: str) -> bool:
    """
    压缩文件夹，返回是否成功。

    Args:
        src_dir (str): 要压缩的源文件夹路径。
        dst_zip (str): 压缩后的目标 ZIP 文件路径（不需要扩展名）。

    Returns:
        bool: 压缩是否成功。
    """
    try:
        shutil.make_archive(dst_zip, 'zip', src_dir)
        return True
    except Exception as e:
        print(f"压缩文件夹失败: {e}")
        return False

@mcp.tool()
async def get_all_files(folder_path: str) -> List[str]:
    """
    获取指定文件夹下的所有文件路径（包括子文件夹中的文件）。

    Args:
        folder_path (str): 要遍历的文件夹路径。

    Returns:
        List[str]: 所有文件的完整路径列表。
    """
    try:
        all_files = []
        # 递归遍历文件夹
        for root, _, files in os.walk(folder_path):
            for file in files:
                # 拼接文件的完整路径
                file_path = os.path.join(root, file)
                all_files.append(file_path)
        return all_files
    except Exception as e:
        print(f"获取文件夹下所有文件失败: {e}")
        return []

@mcp.tool()
def read_text_from_file(file_path: str) -> Union[str, None]:
    """
    从文件中读取文本内容，支持多种文本文件格式。

    Args:
        file_path (str): 文件的完整路径。

    Returns:
        Union[str, None]: 文件中的文本内容。如果文件格式不支持或读取失败，返回 None。
    """
    try:
        # 检查文件是否存在
        if not os.path.exists(file_path):
            print(f"文件不存在: {file_path}")
            return None

        # 获取文件扩展名
        _, file_ext = os.path.splitext(file_path)

        # 读取纯文本文件
        if file_ext in (".txt", ".log", ".md", ".ini", ".cfg", ".sql", ".bat", ".sh"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        # 读取 JSON 文件
        elif file_ext == ".json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return json.dumps(data, indent=4, ensure_ascii=False)

        # 读取 XML 文件
        elif file_ext == ".xml":
            tree = ET.parse(file_path)
            root = tree.getroot()
            return ET.tostring(root, encoding="unicode")

        # 读取 CSV 或 TSV 文件
        elif file_ext in (".csv", ".tsv"):
            delimiter = "," if file_ext == ".csv" else "\t"
            with open(file_path, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=delimiter)
                return "\n".join([delimiter.join(row) for row in reader])

        # 读取 Excel 文件
        elif file_ext in (".xlsx", ".xls"):
            try:
                df = pd.read_excel(file_path, sheet_name=None)
                return "\n".join([df[sheet].to_string() for sheet in df])
            except Exception as e:
                print(f"读取 Excel 文件失败: {e}")
                return None

        # 读取 Word 文件
        elif file_ext in (".docx", ".doc"):
            try:
                doc = Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
            except Exception as e:
                print(f"读取 Word 文件失败: {e}")
                return None

        # 读取 HTML 文件
        elif file_ext in (".html", ".htm"):
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()

        # 读取 YAML 文件
        elif file_ext in (".yaml", ".yml"):
            try:
                import yaml  # 需要安装 PyYAML 库
                with open(file_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f)
                    return yaml.dump(data, default_flow_style=False, allow_unicode=True)
            except ImportError:
                print("请安装 PyYAML 库以支持 YAML 文件: pip install pyyaml")
                return None
            except Exception as e:
                print(f"读取 YAML 文件失败: {e}")
                return None

        # 不支持的文件格式
        else:
            print(f"不支持的文件格式: {file_ext}")
            return None

    except Exception as e:
        print(f"读取文件失败: {e}")
        return None

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')