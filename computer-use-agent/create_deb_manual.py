#!/usr/bin/env python3
"""
Manual .deb Package Creator for Computer Use Agent
Creates a proper Debian package without needing dpkg-deb on Windows.
"""

import os
import struct
import tarfile
import tempfile
from pathlib import Path
import shutil

def create_ar_archive(output_path, files):
    """Create AR archive format (used by .deb packages)"""
    with open(output_path, 'wb') as ar_file:
        # AR magic number
        ar_file.write(b'!<arch>\n')
        
        for file_path, data in files:
            # File header (60 bytes)
            name = file_path.encode('ascii')
            if len(name) > 16:
                name = name[:16]
            
            # Pad name to 16 bytes
            name = name.ljust(16, b' ')
            
            # File stats (all zeros for our purposes)
            timestamp = b'0'.ljust(12, b' ')
            owner_id = b'0'.ljust(6, b' ')
            group_id = b'0'.ljust(6, b' ')
            mode = b'644'.ljust(8, b' ')
            size = str(len(data)).encode('ascii').ljust(10, b' ')
            
            # Header end marker
            end_marker = b'`\n'
            
            # Write header
            ar_file.write(name + timestamp + owner_id + group_id + mode + size + end_marker)
            
            # Write data
            ar_file.write(data)
            
            # Pad to even boundary
            if len(data) % 2:
                ar_file.write(b'\n')

def create_deb_package():
    """Create .deb package manually"""
    print("🔨 Creating .deb package manually...")
    
    package_dir = Path("linux_package")
    debian_dir = package_dir / "computer-use-agent_1.0.0_amd64"
    
    if not debian_dir.exists():
        print("❌ Debian package directory not found")
        return False
        
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            
            # Create debian-binary file
            debian_binary = b"2.0\n"
            
            # Create control.tar.gz
            control_tar_path = temp_path / "control.tar.gz"
            with tarfile.open(control_tar_path, "w:gz") as control_tar:
                control_dir = debian_dir / "DEBIAN"
                for file_path in control_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(control_dir)
                        control_tar.add(file_path, arcname=arcname)
                        
            # Create data.tar.gz
            data_tar_path = temp_path / "data.tar.gz"
            with tarfile.open(data_tar_path, "w:gz") as data_tar:
                for subdir in ['usr', 'etc']:
                    subdir_path = debian_dir / subdir
                    if subdir_path.exists():
                        for file_path in subdir_path.rglob('*'):
                            if file_path.is_file():
                                arcname = file_path.relative_to(debian_dir)
                                # Preserve file permissions for executables
                                tarinfo = data_tar.gettarinfo(file_path, arcname=str(arcname))
                                if file_path.suffix in ['.sh', ''] and 'bin/' in str(arcname):
                                    tarinfo.mode = 0o755
                                with open(file_path, 'rb') as f:
                                    data_tar.addfile(tarinfo, f)
                                    
            # Read the tar files
            with open(control_tar_path, 'rb') as f:
                control_data = f.read()
                
            with open(data_tar_path, 'rb') as f:
                data_data = f.read()
                
            # Create the .deb package
            deb_path = Path("computer-use-agent_1.0.0_amd64.deb")
            
            files = [
                ('debian-binary', debian_binary),
                ('control.tar.gz', control_data),
                ('data.tar.gz', data_data)
            ]
            
            create_ar_archive(deb_path, files)
            
            print(f"✅ .deb package created: {deb_path}")
            print(f"💾 Package size: {deb_path.stat().st_size / 1024:.1f} KB")
            
            return True
            
    except Exception as e:
        print(f"❌ Failed to create .deb package: {e}")
        return False

if __name__ == "__main__":
    create_deb_package()

