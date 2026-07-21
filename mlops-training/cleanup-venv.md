If you want to **completely remove and recreate the virtual environment (`.venv`)**, follow these steps.

### Step 1: Deactivate the Virtual Environment (if active)

If your terminal shows:

```text
(.venv) E:\ai-training\Enterprise-Mlops\python-lab>
```

Run:

```cmd
deactivate
```

If it says `'deactivate' is not recognized`, just close the terminal or continue to the next step.

---

### Step 2: Delete the `.venv` Folder

Navigate to your project:

```cmd
cd /d E:\ai-training\Enterprise-Mlops\python-lab
```

Delete the `.venv` folder:

**Command Prompt (CMD):**

```cmd
rmdir /s /q .venv
```

**PowerShell:**

```powershell
Remove-Item .venv -Recurse -Force
```

Or simply delete the `.venv` folder from File Explorer.

---

### Step 3: Remove the Jupyter Kernel (Optional)

List installed kernels:

```cmd
jupyter kernelspec list
```

Example output:

```text
Available kernels:
  python3      C:\Users\Venkat\AppData\Roaming\jupyter\kernels\python3
  python-lab   C:\Users\Venkat\AppData\Roaming\jupyter\kernels\python-lab
```

Remove your custom kernel:

```cmd
jupyter kernelspec uninstall python-lab
```

Type `y` to confirm.

---

### Step 4: Remove VS Code Workspace Settings (Optional)

Delete these folders/files if they exist:

```text
E:\ai-training\Enterprise-Mlops\python-lab\.vscode\
```

and

```text
E:\ai-training\Enterprise-Mlops\python-lab\.ipynb_checkpoints\
```

---

### Step 5: Verify Cleanup

Run:

```cmd
dir
```

You should no longer see:

```text
.venv
```

---

### Step 6: Create a Fresh Virtual Environment

```cmd
python -m venv .venv
```

Activate it:

```cmd
.venv\Scripts\activate
```

Install the required packages:

```cmd
python -m pip install --upgrade pip
pip install jupyter notebook ipykernel pandas numpy matplotlib
```

Register the kernel:

```cmd
python -m ipykernel install --user --name python-lab --display-name "Python Lab"
```

---

### Complete Cleanup Commands (CMD)

```cmd
cd /d E:\ai-training\Enterprise-Mlops\python-lab

deactivate

rmdir /s /q .venv

jupyter kernelspec uninstall python-lab
```

Then recreate:

```cmd
python -m venv .venv

.venv\Scripts\activate

python -m pip install --upgrade pip

pip install jupyter notebook ipykernel pandas numpy matplotlib

python -m ipykernel install --user --name python-lab --display-name "Python Lab"
```

This will give you a completely fresh Python virtual environment for your project.
