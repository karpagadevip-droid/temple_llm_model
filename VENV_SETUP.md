# Virtual Environment Setup Guide

## Virtual Environment Created

A Python virtual environment has been created in `d:\Devi Tech\venv\`

## How to Activate the Virtual Environment

### Method 1: Bypass PowerShell Execution Policy (Recommended)

Instead of using the `.ps1` script, use this command to activate:

```powershell
venv\Scripts\activate.bat
```

This uses the batch file instead of PowerShell script and bypasses the execution policy restriction.

### Method 2: Temporarily Allow PowerShell Scripts (Current Session Only)

If you prefer to use the PowerShell activation script:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
venv\Scripts\Activate.ps1
```

This temporarily allows scripts for the current PowerShell session only (doesn't affect system settings).

### Method 3: Direct Python Execution

You can also run Python directly from the virtual environment without activating:

```powershell
venv\Scripts\python.exe temple_generator.py
```

## Installing Packages in Virtual Environment

Once activated (or using Method 3), install the required package:

```powershell
# If activated with Method 1 or 2:
pip install wikipedia

# If using Method 3 (not activated):
venv\Scripts\pip.exe install wikipedia
```

## Running the Temple Generator Script

### Option A: With Activated Virtual Environment

```powershell
# Activate first
venv\Scripts\activate.bat

# Install dependencies
pip install wikipedia

# Run the script
python temple_generator.py

# Deactivate when done
deactivate
```

### Option B: Without Activating (Direct Execution)

```powershell
# Install dependencies
venv\Scripts\pip.exe install wikipedia

# Run the script
venv\Scripts\python.exe temple_generator.py
```

## Verifying Virtual Environment

To check if you're in the virtual environment:

```powershell
# Your prompt should show (venv) at the beginning
# Example: (venv) PS D:\Devi Tech>

# Or check Python location:
where python
# Should show: D:\Devi Tech\venv\Scripts\python.exe
```

## Why Use a Virtual Environment?

✅ **Isolated Dependencies**: Packages installed here won't affect your global Python installation
✅ **Project-Specific**: Each project can have its own package versions
✅ **Clean Management**: Easy to delete and recreate if needed
✅ **Reproducibility**: Makes it easier to share your project with others

## Quick Reference

| Action | Command |
|--------|---------|
| Activate (Batch) | `venv\Scripts\activate.bat` |
| Activate (PowerShell) | `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process` then `venv\Scripts\Activate.ps1` |
| Deactivate | `deactivate` |
| Install Package | `pip install package_name` |
| Run Script | `python temple_generator.py` |
| Direct Python | `venv\Scripts\python.exe temple_generator.py` |

## Note

The script has already been successfully executed using your global Python installation. The virtual environment is now set up for future runs and better package management.
