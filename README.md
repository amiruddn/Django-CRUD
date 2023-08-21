# Django-CRUD

# **Vulcan Process**

##### Authors:
##### 1. Michael Chuang (jazzdivined)
##### 2. Kevin Jonathan (caveinjoe)
<br>

> ### Table of Contents
>
> 1. [Creating a Machine Template](#creating-a-machine-template)
>       * [Setting up a new Machine Template](#setting-up-a-new-machine-template)
>       * [First Look at the Machine Template](#first-look-at-the-machine-template)
>       * [Creating a New Command](#creating-a-new-command)
> 3. [Registering a Machine Template to Views](#registering-a-machine-template-to-views)
> 4. [A Reminder to Always Take A Break](#a-reminder-to-always-take-a-break)

<br>

## **Creating a Machine Template**

___

To create a program with Vulcan, a `Machine Template` is needed. The logic and algorithms required for all machines will reside in this `Machine Template`. 

*Note: All Machine Templates are located in the directory `process_template`.*


### ***Setting up a new Machine Template***

Run the following in the terminal while in the directory `vulcan_process`

```commandline
python manage.py new_template <name> <version>
```

The new Machine Template should be created and placed within the directory `process_template` which will look like the following. 

```txt
process_template
|
+-- <name>
|   +-- v<version>
|   |   +-- __init__.py
|   |   +-- tasks.py
|   |
+-- other_machine_template
|   +-- neglected_machine_folder_1
|   +-- neglected_machine_folder_2
```

We will now create a new Machine Template named `asrs`. 

Firstly, call the following command in the terminal

```commandline
python manage.py new_template <name> <version_number>
```

Example:

```commandline
python manage.py new_template asrs 1
```

A new file will then be created within `process_template`, which should now look like the following.

```txt
process_template
|
+-- asrs
|   +-- v1
|   |   +-- __init__.py
|   |   +-- tasks.py
|   |
+-- other_machine_template
|   +-- neglected_machine_folder_1
|   +-- neglected_machine_folder_2
```

*Note: Call the same command with the same name and a different version to create a new version of a Machine Template*

### ***First look at the Machine Template***

There are two important files within every Machine Template, namely `__init.py__` and `tasks.py`. 

Here's a look at the contents of the files created from the example given in [Setting up a new Machine Template](#setting-up-a-new-machine-template)

`__init__.py`
```python
class AsrsVersion1(MachineTemplate):
    def __init__(self, identity: dict = None, constants_value: dict = None):
        super().__init__(identity, constants_value)

    @classmethod
    @extend_list_commands
    def list_commands(cls) -> list:
        return ["custom_command1", "custom_command2"]

    @classmethod
    def list_constants(cls) -> list:
        return ["pin", "constant1", "constant2"]

    @async_task(asrs_custom_command1)
    def custom_command1(self):
        return {
            "talos_id": self.talos_id,
            "constant1": self._constants_value["constant1"]
        }

    @async_task(asrs_custom_command2)
    def custom_command2(self):
        return {
            "talos_id": self.talos_id,
            "pin": self._constants_value["pin"]
            "constant2": self._constants_value["constant2"]
        }

    @async_task(asrs_run)
    def run(self):
        return {
            "talos_id": int(self.talos_id),
            "pin": self._constants_value['pin']
        }
```

`tasks.py`
```python
from celeries.celery import app
from packages.talos.core import Talos

@app.task(bind=True)
def asrs_custom_command1(self, talos_id, constant1: int):
    talos: Talos = Talos.find_by_id(talos_id)
    print(f"ID: {talos_id}|{type(talos_id)}")
    print(f"Talos Instances: {Talos.instances}")
    print(f"Initialize_talos Find_by_id: {talos}")
    res = talos.digital_write(0, 0)
    self.update_state(state='SUCCESS',
                      meta={"message": f"{res}"})

@app.task(bind=True)
def asrs_custom_command2(self, talos_id, pin: int, constant2: int):
    talos: Talos = Talos.find_by_id(talos_id)
    print(f"ID: {talos_id}|{type(talos_id)}")
    print(f"Talos Instances: {Talos.instances}")
    print(f"Initialize_talos Find_by_id: {talos}")
    if constant2 > 5:
        res = talos.digital_write(pin, 0)
    else:
        res = talos.digital_write(pin, 1)
    self.update_state(state='SUCCESS',
                      meta={"message": f"{res}"})

@app.task(bind=True)
def asrs_run(self, talos_id, pin: int):
    talos: Talos = Talos.find_by_id(talos_id)
    while True:
        print("Hello World!")

```

### ***Creating a New Command***

#### **Step 1**
Firstly, head to `tasks.py` of the newly created Machine Template and add a new function with the following format.

```python
@app.task(bind=True)
def new_custom_command(self, talos_id, constant: int, pin: int):
    talos: Talos = Talos.find_by_id(talos_id)
    print(f"ID: {talos_id}|{type(talos_id)}")
    print(f"Talos Instances: {Talos.instances}")
    print(f"Initialize_talos Find_by_id: {talos}")

    # Insert Talos Command(s) and other logic/algorithm(s) HERE

    self.update_state(state='SUCCESS',
                      meta={"message": f"RESPONSE HERE"})
```
For example, the following command from the [previous example](#first-look-at-the-machine-template) turns a digital pin on or off depending on a constant

```python
@app.task(bind=True)
def asrs_custom_command2(self, talos_id, pin: int, constant2: int):
    talos: Talos = Talos.find_by_id(talos_id)
    print(f"ID: {talos_id}|{type(talos_id)}")
    print(f"Talos Instances: {Talos.instances}")
    print(f"Initialize_talos Find_by_id: {talos}")
    if constant2 > 5:
        res = talos.digital_write(pin, 0)
    else:
        res = talos.digital_write(pin, 1)
    self.update_state(state='SUCCESS',
                      meta={"message": f"{res}"})
```
Note that all pins and constants used should be included in the parameters of the function

#### **Step 2**

Import the function into `__init__.py`

Then, add a method in the class within `__init__.py` with a name used to represent the `callable` function that was defined in the [previous step](#step-1), decorating it with `@async_task(imported_function)`

```python
    @async_task(new_custom_command)
    def new_custom_command(self):
        return {
            "talos_id": self.talos_id,
            "pin": self._constants_value["pin"]
            "constant": self._constants_value["constant"]
        }
```
Using the example from the [previous step](#step-1), the method will look like the following

```python
    @async_task(asrs_custom_command2)
    def custom_command2(self):
        return {
            "talos_id": self.talos_id,
            "pin": self._constants_value["pin"]
            "constant2": self._constants_value["constant2"]
        }
```
> It is important to note that the `keys` of the returned dictionary MUST have the same name as the parameters used in the function defined in [Step 1](#step-1)

#### **Step 3**

Finally, append the names of all methods that should be shown in the Admin Model into the method `list_commands` and all variables used into `list_constants`

```python
@classmethod
    @extend_list_commands
    def list_commands(cls) -> list:
        return ["custom_command1", "custom_command2"]
```

This method makes it possible to show the listed commands into the Admin Model

```python
@classmethod
    def list_constants(cls) -> list:
        return ["pin", "constant1", "constant2"]
```
This method makes it possible to define and retrieve the listed constants from the Admin Model
___

<br>

## **Registering a Machine Template to Views**

___

Now comes the easiest part, connecting the Machine Template to the Admin Model.

Import the class from the newly created `Machine Template`

Then, create a new class within `views.py` in the directory `process_api`

```python
from process_template.new_machine_template.v1 import NewMachineTemplateVersion1

class NewMachineTemplateView(MachineTemplateView)
    versions = {
        1: NewMachineTemplateVersion1
    }
```
Add the new class into the list `register_views`
```python
register_views = [
    ConveyourView, BlinkerView, NewMachineTemplateView
]
```
For example,
```python
from process_api.abstract import MachineTemplateView
from process_template.blinker.v1 import BlinkerVersion1
from process_template.load_cell_conveyour.v1 import ConveyourVersion1


class BlinkerView(MachineTemplateView):
    versions = {
        1: BlinkerVersion1
    }


class ConveyourView(MachineTemplateView):
    versions = {
        1: ConveyourVersion1
    }


class AsrsView(MachineTemplateView)
    versions = {
        1: ConveyourVersion1
    }


register_views = [
    ConveyourView, BlinkerView, AsrsView
]
```
___

<br>

## **A Reminder to Always Take A Break**

___

Congratulations on making it this far, but there are more to come. Like, way more. It never ends. Writing this sacrifices our time to spend it with our significant others. Both of the writers need to go on a date. No no no, no homo. We identify ourselves as attack copters.

In any case, it is HIGHLY recommended to take a break before programming or heading over to Vulcan Production.

<img src="https://media.tenor.com/ANQ5MHKx7EYAAAAC/star-wars-dark-side.gif" width="300">

Please remember to pray to your God for guidance if
anything goes wrong. Other than that, please take care
of your health.

<img src="https://i.kym-cdn.com/photos/images/newsfeed/001/688/917/f1e.jpg" width="300">

___
