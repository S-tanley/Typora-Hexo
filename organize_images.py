import os
import shutil
from pathlib import Path

def find_deepest_numeric_folders(root_path):
    """
    找到所有以数字开头的父文件夹路径中最深的子文件夹
    示例：public/2025/03/25/test-post → 定位到 test-post 所在的父层级 2025/03/25
    """
    target_parents = set()
    
    # 遍历所有可能的目录
    for dirpath, dirnames, _ in os.walk(root_path):
        path_parts = Path(dirpath).relative_to(root_path).parts
        
        # 检查路径中的每一层是否以数字开头
        numeric_chain = []
        for part in path_parts:
            if part[0].isdigit():
                numeric_chain.append(part)
            else:
                break  # 遇到非数字开头则终止
        
        # 记录以数字开头的路径中第三层父目录
        if len(numeric_chain) == 3:
            deepest_parent = Path(root_path).joinpath(*numeric_chain)
            target_parents.add(str(deepest_parent))
    
    return target_parents

def move_images_to_subfolder(public_path="public"):
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp')
    target_parents = find_deepest_numeric_folders(public_path)
    
    for parent in target_parents:
        parent_path = Path(parent)
        
        for post_dir in parent_path.iterdir():
            if post_dir.is_dir():
                post_name = post_dir.name
                target_subdir = post_dir / post_name
                
                # 检查当前目录是否有图片
                has_images = any(
                    file.is_file() and file.suffix.lower() in image_extensions
                    for file in post_dir.iterdir()
                )
                
                if not has_images:
                    continue  # 没有图片则跳过
                
                # 创建子目录并移动图片
                target_subdir.mkdir(exist_ok=True)
                for file in post_dir.iterdir():
                    if file.is_file() and file.suffix.lower() in image_extensions:
                        shutil.move(str(file), str(target_subdir / file.name))

if __name__ == "__main__":
    move_images_to_subfolder()
    print("图片整理完成！")
