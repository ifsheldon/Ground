## Test

1. run `server.py` in background
2. open `ip:5000` in browser
3. open `hack.ipynb`

## What can be done?

- Change LR with time
- Change any value with time

## Use

### Config File
```
key = setting item
value = time -> value
```
```json
{
    "learning_rate": {
        "0": 1,
        "10": 0.8
    },
    "cond": {
        "0": false,
        "20": true,
        "50": false
    }
}
```

### In training

```python
# create a scheduler
# need to specify the file path
my_path = "a.json"
scheduler3 = MyFileLR(optimizer, my_path)

# create some placeholders for variables to be used later
scheduler3.cond =True

# update those variables with initial value
scheduler3._update_other_var()

for epoch in range(10000):

    print(epoch, optimizer.param_groups[0]["lr"])

    # now it should work
    if scheduler3.cond:
        print("cond true")
    else:
        print("cond false")
    
    optimizer.step()
    scheduler3.step()

    # for visualize
    sleep(1)
```