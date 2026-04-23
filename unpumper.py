import os
import sys
import time
import mmap
import math
import ctypes
from pathlib import Path

class NarokUnpumper:
    def __init__(self):
        self.lang_id = ctypes.windll.kernel32.GetUserDefaultUILanguage()
        self.is_thai = (self.lang_id == 1054)
        self.chunk_size = 1024 * 1024 * 8  # 8MB Optimized Buffer
        
        self.msg = {
            "title": "NAROK - UNPUMPER TOOL",
            "ver": "v2.0 [ By Sashimi_Dev ]",
            "usage": "Usage: Drag & Drop files onto this tool" if not self.is_thai else "วิธีใช้: ลากไฟล์หลายๆ ไฟล์มาวางที่นี่เพื่อเริ่มทำงาน",
            "analyzing": "[*] Analyzing: " if not self.is_thai else "[*] กำลังวิเคราะห์: ",
            "orig_size": "[*] Original Size: " if not self.is_thai else "[*] ขนาดเดิม: ",
            "scanning": "[*] Scanning for null-padding..." if not self.is_thai else "[*] กำลังค้นหาข้อมูลขยะ...",
            "clean": "[!] File is already clean: " if not self.is_thai else "[!] ไฟล์นี้สะอาดอยู่แล้ว: ",
            "success": "[+] Success! Saved as: " if not self.is_thai else "[+] สำเร็จ! บันทึกไฟล์ใหม่ในชื่อ: ",
            "removed": "[-] Data Stripped: " if not self.is_thai else "[-] ลบขยะออกไปได้: ",
            "final": "[+] Final Size: " if not self.is_thai else "[+] ขนาดสุทธิ: ",
            "efficiency": "[+] Efficiency: " if not self.is_thai else "[+] ลดขนาดไปได้: ",
            "time": "[+] Time Taken: " if not self.is_thai else "[+] เวลาที่ใช้: ",
            "error_perm": "[-] Error: Permission denied (File in use?)" if not self.is_thai else "[-] ผิดพลาด: การเข้าถึงถูกปฏิเสธ (ไฟล์กำลังถูกใช้งานอยู่หรือไม่?)",
            "exit": "\nPress Enter to exit..." if not self.is_thai else "\nกด Enter เพื่อออก..."
        }

    def format_size(self, size_bytes):
        if size_bytes == 0: return "0 B"
        units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        i = min(i, len(units) - 1)
        p = math.pow(1024, i)
        return f"{round(size_bytes / p, 2)} {units[i]}"

    def print_banner(self):
        banner = f"""
    ╔════════════════════════════════════════════════════════╗
    ║             {self.msg['title']}                        ║
    ║             {self.msg['ver']}                          ║
    ╚════════════════════════════════════════════════════════╝
        """
        print(banner)

    def process_file(self, input_path):
        p = Path(input_path)
        if not p.is_file():
            return

        print(f"\n{self.msg['analyzing']}{p.name}")
        try:
            orig_size = p.stat().st_size
            print(f"{self.msg['orig_size']}{self.format_size(orig_size)}")
            
            start_time = time.perf_counter()

            actual_end = 0
            with open(p, 'rb') as f:
                if orig_size > 0:
                    with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
                        pos = orig_size - 1
                        while pos >= 0 and mm[pos] == 0:
                            pos -= 1
                        actual_end = pos + 1

            if actual_end >= orig_size:
                print(f"{self.msg['clean']}{p.name}")
                return

            output_name = f"CLEANED_{p.name}"
            output_path = p.parent / output_name
            
            with open(p, 'rb') as f_in, open(output_path, 'wb') as f_out:
                remaining = actual_end
                while remaining > 0:
                    chunk = f_in.read(min(remaining, self.chunk_size))
                    if not chunk: break
                    f_out.write(chunk)
                    remaining -= len(chunk)
                    print(".", end="", flush=True)

            duration = time.perf_counter() - start_time
            new_size = output_path.stat().st_size
            saved = orig_size - new_size

            print("\n" + "─" * 50)
            print(f"{self.msg['success']}{output_name}")
            print(f"{self.msg['removed']}{self.format_size(saved)}")
            print(f"{self.msg['final']}{self.format_size(new_size)}")
            print(f"{self.msg['efficiency']}-{((saved/orig_size)*100):.2f}%")
            print(f"{self.msg['time']}{duration:.4f} s")
            print("─" * 50)

        except PermissionError:
            print(f"\n{self.msg['error_perm']}")
        except Exception as e:
            print(f"\n[-] Error: {e}")

if __name__ == "__main__":
    tool = NarokUnpumper()
    tool.print_banner()
    
    target_files = sys.argv[1:]
    
    if target_files:
        for file_path in target_files:
            tool.process_file(file_path)
    else:
        print(f"  {tool.msg['usage']}")
    
    input(tool.msg['exit'])