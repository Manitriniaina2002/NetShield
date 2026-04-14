# 🐧 WSL2 Setup for NetShield Cracking Features

Great! You have WSL installed. Now we need to install the cracking tools inside WSL so NetShield can use them.

## Quick Setup (Copy & Paste)

### Step 1: Open WSL Terminal

```bash
# From Windows PowerShell or Command Prompt, run:
wsl
```

This opens your WSL2 Linux terminal.

### Step 2: Install Required Tools

Paste all these commands at once in your WSL terminal:

```bash
# Update package manager
sudo apt update

# Install aircrack-ng suite (for WiFi cracking)
sudo apt install -y aircrack-ng

# Install hashcat (GPU cracking)
sudo apt install -y hashcat

# Install John the Ripper
sudo apt install -y john

# Verify installations
echo "Checking installations..."
which aircrack-ng && echo "✓ aircrack-ng installed"
which hashcat && echo "✓ hashcat installed"  
which john && echo "✓ john installed"
```

### Step 3: Create Wordlist Directory (Optional)

```bash
# Create directory for wordlists
mkdir -p ~/.wordlists
cd ~/.wordlists

# Download rockyou wordlist (if available in WSL)
# This is a popular password dictionary
```

## Verification

### Check if NetShield Detects the Tools

In your backend terminal, you should see:

```
[✓] Available cracking methods:
  • aircrack-ng - via WSL2
  • hashcat - via WSL2 (if NVIDIA GPU)
  • john - via WSL2
```

### Test Manually

In WSL terminal:

```bash
aircrack-ng --version
hashcat --version
john --version
```

All three should show version information.

---

## 🚀 Back in NetShield

After installing tools in WSL:

1. **Restart the backend**:
   - Close the backend terminal (Ctrl+C)
   - Run it again: `start_real_mode.bat`

2. **In the web interface**:
   - Go to **Cracking** tab
   - Try cracking a network
   - Tools should now work via WSL!

---

## Troubleshooting

### Problem: Tools not found even after install

**Solution**:
```bash
# Verify WSL is running properly
wsl --list --verbose

# Should show your distro with STATUS "Running"
```

### Problem: Installation fails

**Solution**:
```bash
# Try updating first
sudo apt update
sudo apt upgrade

# Then install again
sudo apt install aircrack-ng hashcat john
```

### Problem: Permission errors

**Solution**:
```bash
# You might need sudo for some operations
sudo aircrack-ng --version
```

### Problem: WSL not found

**Solution**:
```powershell
# In PowerShell (as Administrator)
wsl --install

# May require restart
Restart-Computer
```

---

## WSL2 Architecture

When you use a cracking tool in NetShield on Windows:

```
Windows (NetShield)
    ↓
wsl [command]  ← NetShield calls this
    ↓
WSL2 Ubuntu/Debian
    ↓
aircrack-ng / hashcat / john
    ↓
Result returned to Windows
```

This is seamless and works in the background!

---

## Performance Notes

- **First run**: Might be slightly slower (WSL startup)
- **Subsequent runs**: Same speed as native Linux
- **GPU cracking**: Works if your GPU is supported by WSL2 (NVIDIA, AMD on specific configurations)

---

## After Installation

You should be able to:

✅ Scan real WiFi networks on Windows
✅ Analyze vulnerabilities
✅ Generate recommendations  
✅ **Crack passwords using WSL2 tools**
✅ Generate audit reports

---

## Commands Quick Reference

| Action | Command |
|--------|---------|
| Open WSL | `wsl` |
| Run command in WSL from Windows | `wsl [command]` |
| Install package | `sudo apt install [package]` |
| Check tool version | `[tool] --version` |
| Exit WSL | `exit` |

---

## Security Note

The cracking tools work in read-only mode on the captured handshakes. They:
- ✅ Only process handshake files you provide
- ✅ Do not modify your network
- ✅ Use standard dictionary/wordlist attacks
- ✅ Are safe to use on your own networks or authorized testing

---

## Next Steps

1. Install tools in WSL (see Step 2 above)
2. Restart NetShield backend
3. Go to **Cracking** tab in web interface
4. Select **aircrack-ng** or **hashcat** method
5. Upload handshake file (or use simulated for testing)
6. Watch the real cracking progress!

---

**Ready? Open WSL and run the install commands above!** 🎯
