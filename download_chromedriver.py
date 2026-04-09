import os
import subprocess
import re
import platform
import urllib.request
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).parent


def get_chrome_version():
    system = platform.system()
    
    if system == "Windows":
        try:
            result = subprocess.run(
                r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version',
                capture_output=True, text=True, shell=True
            )
            match = re.search(r'veg\s+REG_SZ\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
        except:
            pass
        
        try:
            paths = [
                r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Google\\Chrome\\Application\\chrome.exe")
            ]
            for path in paths:
                if os.path.exists(path):
                    result = subprocess.run(f'"{path}" --version', capture_output=True, text=True, shell=True)
                    match = re.search(r'Chrome\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
                    if match:
                        return match.group(1)
        except:
            pass
    
    elif system == "Darwin":
        result = subprocess.run(
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --version",
            capture_output=True, text=True, shell=True
        )
        match = re.search(r'Chrome\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
        if match:
            return match.group(1)
    
    elif system == "Linux":
        result = subprocess.run("google-chrome --version", capture_output=True, text=True, shell=True)
        match = re.search(r'Chrome\s+(\d+\.\d+\.\d+\.\d+)', result.stdout)
        if match:
            return match.group(1)
    
    return None


def get_chromedriver_url(chrome_version):
    major_version = chrome_version.split('.')[0]
    
    base_url = f"https://chromedriver.storage.googleapis.com"
    
    try:
        index_url = f"{base_url}/"
        response = urllib.request.urlopen(index_url, timeout=10)
        content = response.read().decode()
        
        pattern = rf'chrome{major_version}[^"]*\.zip'
        match = re.search(pattern, content)
        
        if match:
            return f"{base_url}/{match.group()}"
        
        for version in range(int(major_version), int(major_version) - 10, -1):
            try:
                version_url = f"{base_url}/LATEST_RELEASE_{version}"
                req = urllib.request.Request(version_url)
                response = urllib.request.urlopen(req, timeout=5)
                actual_version = response.read().decode().strip()
                
                return f"{base_url}/{actual_version}/chromedriver_{'win32' if platform.system() == 'Windows' else ('mac_arm64' if platform.system() == 'Darwin' and platform.machine() == 'arm64' else 'mac64' if platform.system() == 'Darwin' else 'linux64'}.zip"
            except:
                continue
    
    except Exception as e:
        print(f"获取版本信息失败: {e}")
    
    return None


def download_chromedriver():
    print("检测 Chrome 版本...")
    version = get_chrome_version()
    
    if not version:
        print("无法自动检测 Chrome 版本，请手动下载")
        print("访问: https://chromedriver.chromium.org/downloads")
        return False
    
    print(f"检测到 Chrome 版本: {version}")
    
    major_version = version.split('.')[0]
    print(f"正在获取 ChromeDriver for Chrome {major_version}...")
    
    system = platform.system()
    if system == "Windows":
        driver_name = "chromedriver.exe"
        platform_str = "win32"
    elif system == "Darwin":
        if platform.machine() == "arm64":
            driver_name = "chromedriver"
            platform_str = "mac_arm64"
        else:
            driver_name = "chromedriver"
            platform_str = "mac64"
    else:
        driver_name = "chromedriver"
        platform_str = "linux64"
    
    try:
        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        req = urllib.request.Request(url)
        response = urllib.request.urlopen(req, timeout=10)
        driver_version = response.read().decode().strip()
        
        download_url = f"https://chromedriver.storage.googleapis.com/{driver_version}/chromedriver_{platform_str}.zip"
        
        zip_path = BASE_DIR / "chromedriver.zip"
        print(f"下载 ChromeDriver: {download_url}")
        
        urllib.request.urlretrieve(download_url, zip_path)
        print("下载完成，正在解压...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(BASE_DIR)
        
        os.remove(zip_path)
        
        driver_path = BASE_DIR / driver_name
        if driver_path.exists():
            if platform.system() != "Windows":
                os.chmod(driver_path, 0o755)
            print(f"ChromeDriver 已安装到: {driver_path}")
            return True
    
    except Exception as e:
        print(f"下载失败: {e}")
        return False
    
    return False


if __name__ == "__main__":
    download_chromedriver()
