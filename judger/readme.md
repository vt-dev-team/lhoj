### LHOJ Judger

Using python to judge, without **any safety measures**.

#### Installation

```bash
pip install psutil requests
python main.py
```

#### Working Principle

1. Using Judge Account to login (This account must have permission to download data and modify evaluation results）, now we get cookies
2. Ask for the latest submission on the backend.
3. Copying user code, input and output file to tmp folder.
4. Running Code and Judging it.
5. Sleep and then goto 2

#### Contribution

Just do your self.
