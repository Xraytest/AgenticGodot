#!/usr/bin/env python3
"""
Remote Linux Build via plink - non-interactive SSH build
"""
import os, sys, subprocess, argparse, logging, tempfile, time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('PlinkBuild')

PLINK = r"C:\Program Files\PuTTY\plink.exe"

def plink_cmd(host, port, username, password, cmd, timeout=600):
    """Execute command via plink with password"""
    full_cmd = [
        PLINK, "-ssh", "-batch",
        "-hostkey", "ssh-ed25519 255 SHA256:C3T/odnbnYflzpQEVGb6GMtu6V7VEyRfI62Bp6Aa9Ik",
        "-pw", password,
        "-P", str(port),
        f"{username}@{host}",
        cmd
    ]
    logger.info(f"[>] {cmd[:100]}...")
    try:
        result = subprocess.run(
            full_cmd,
            capture_output=True, text=True,
            timeout=timeout
        )
        if result.returncode == 0:
            if result.stdout.strip():
                for line in result.stdout.strip().split('\n')[-5:]:
                    logger.info(f"[<] {line.strip()}")
            return True, result.stdout
        else:
            logger.error(f"[!] Exit code {result.returncode}")
            if result.stderr:
                for line in result.stderr.strip().split('\n')[-3:]:
                    logger.error(f"[!] {line.strip()}")
            return False, result.stderr
    except subprocess.TimeoutExpired:
        logger.error("[!] Command timed out")
        return False, "timeout"

def cache_host_key(host, port, username, password):
    """Cache host key by attempting a connection"""
    logger.info(f"[*] Caching host key for {host}:{port}...")
    cmd = [
        PLINK, "-ssh", "-batch",
        "-hostkey", "ssh-ed25519 255 SHA256:C3T/odnbnYflzpQEVGb6GMtu6V7VEyRfI62Bp6Aa9Ik",
        "-pw", password, "-P", str(port),
        f"{username}@{host}", "echo CACHED_OK"
    ]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if r.returncode == 0:
            logger.info("[+] Host key cached")
            return True
        else:
            logger.warning(f"[!] Cache failed: {r.stderr[:200]}")
    except Exception as e:
        logger.warning(f"[!] Cache exception: {e}")
    return False

def main():
    parser = argparse.ArgumentParser(description='Remote Linux Godot Build via plink')
    parser.add_argument('--host', default='192.168.1.3')
    parser.add_argument('--port', type=int, default=22)
    parser.add_argument('--username', default='xray4668')
    parser.add_argument('--password', default='18248745')
    parser.add_argument('--arch', default='x86_64')
    parser.add_argument('--target', default='release')
    parser.add_argument('--skip-setup', action='store_true')
    args = parser.parse_args()

    if not os.path.exists(PLINK):
        logger.error(f"[!] plink not found at {PLINK}")
        sys.exit(1)

    cache_host_key(args.host, args.port, args.username, args.password)

    remote_dir = '/tmp/agentic_godot_build'
    repo_url = 'https://github.com/Xraytest/AgenticGodot.git'

    steps = []

    if not args.skip_setup:
        steps.append(f"mkdir -p {remote_dir} && export PATH=$HOME/.local/bin:$PATH && python3 -m scons --version 2>&1 | head -1")

    steps.append(
        f"export PATH=$HOME/.local/bin:$PATH && "
        f"cd {remote_dir} && "
        f"[ -d godot ] || git clone --depth 1 --branch main {repo_url} godot 2>&1; "
        f"cd godot/godot_source && "
        f"python3 -m scons platform=linuxbsd target={args.target} arch={args.arch} "
        f"disable_3d=no progress=yes -j$(nproc) 2>&1"
    )

    steps.append(f"ls -la {remote_dir}/godot/godot_source/bin/ 2>&1")

    # Copy binary back via plink/pscp
    exe_name = f"godot.linuxbsd.{args.target}.{args.arch}"
    steps.append(
        f"cp {remote_dir}/godot/godot_source/bin/{exe_name} "
        f"{remote_dir}/godot/build/godot_linux_{args.arch} 2>&1"
    )

    for i, cmd in enumerate(steps):
        logger.info(f"[*] Step {i+1}/{len(steps)}")
        success, output = plink_cmd(args.host, args.port, args.username, args.password, cmd, timeout=1800)
        if not success:
            logger.error(f"[!] Step {i+1} failed")
            sys.exit(1)

    # Download the binary using pscp
    pscp = os.path.join(os.path.dirname(PLINK), "pscp.exe")
    local_build = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build")
    os.makedirs(local_build, exist_ok=True)

    download_cmd = [
        pscp, "-scp", "-batch",
        "-hostkey", "ssh-ed25519 255 SHA256:C3T/odnbnYflzpQEVGb6GMtu6V7VEyRfI62Bp6Aa9Ik",
        "-pw", args.password,
        "-P", str(args.port),
        f"{args.username}@{args.host}:{remote_dir}/godot/godot_source/bin/{exe_name}",
        local_build + "/"
    ]
    logger.info(f"[*] Downloading binary...")
    try:
        subprocess.run(download_cmd, check=True, timeout=120)
        logger.info(f"[+] Binary saved to {local_build}/godot_linux_{args.arch}")
    except Exception as e:
        logger.error(f"[!] Download failed: {e}")
        sys.exit(1)

    logger.info("[+] BUILD COMPLETE")

if __name__ == "__main__":
    main()