## OS
Linux only!
Something strange with multiprocess currently on Windows. 

## Prereq

```
web.py
pytorch
```

```
pip install web.py
```

Thanks to `argparseweb`[Github](https://github.com/nirizr/argparseweb)

## Test

1. run `demo.py`
2. open `ip:8080` in browser
(Opt) open `hack.ipynb`

## What can be done?

- Change LR with time (a special case, directly changing `optim.config`)
- Change any value with time (need to use attribute from the specific scheduler, not elegant yet...)
- Revert to a previous state
- Change parameter during init (the same way of using `argparse`, thanks to `argparseweb`)
- One thread for init & runtime

## Use

### Config File
Currently hardcoded `a.json`.

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

### Initialization

```python
for opts in webui.Webui(parser, title="My Awesome Model trainer!").get():
    print("options as a dict: ", opts)
    print("Hello {name},\nthis is a simple example.".format(name=opts.name))
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