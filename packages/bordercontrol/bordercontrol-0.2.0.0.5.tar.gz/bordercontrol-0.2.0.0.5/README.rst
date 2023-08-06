.. image:: https://travis-ci.com/hardenchant/nats_scan_wrapper.svg?token=oEYn8ZVFWCpj1fwzyy2Q&branch=master
    :target: https://travis-ci.com/hardenchant/nats_scan_wrapper
    :alt: Build status for the master branch

.. image:: https://img.shields.io/pypi/v/bordercontrol.svg
    :target: https://pypi.org/project/bordercontrol/
    :alt: Latest version on PyPi

----------------------------------------------------
Instruction for develop a new module.
----------------------------------------------------

.. code-block:: python

    from bc.dev.handlers import WorkerThreadHandler

    counter = 0

    def worker_function(data):
        global counter
        counter += 1
        print(counter)

        return {"results": [1, 2, 3, 45]}

    a = WorkerThreadHandler(worker_function=worker_function, name='name', hostname='hostname')
    a.run()


**worker_function** - required arg

**name** - optional

**hostname** - optional

**data** - here you see all data which send in sheduler in your channel, e.g.:

.. code-block:: json

    {
       "_id":"5c4f3c5e1a169100074132ca",
       "pipeline":[
            "tgchecker"
       ],
       "crontab":"* * * * *",
       "payload":{
            "integram_url": "",
            "text": ""
       },
       "active": false,
       "trigger_timestamp": 1548696730,
       "full_pipeline":[
            "tgchecker"
       ]
    }

**{"results": [1, 2, 3, 45]}** - module send to channel `_reporter` as:

.. code-block:: python

    {
        'task_data': data,
        'result': [1, 2, 3, 45],
        'name': 'name',
        'hostname': 'hostname'
    }


Module send to channel `_registration`:

.. code-block:: json

    {
        "name": "name",
        "hostname": "hostname"
    }


Module must receive from channel `_registration`:

.. code-block:: python

    {
        'subjects_to_subscribe': ['test'],
        'unique_name': 'test_module1'
    }


If error will be detected in worker, module send error message to channel `_errors`:

.. code-block:: python

    {
        'task_data': data,
        'result': "ERROR",
        'name': 'name',
        'hostname': 'hostname'
    }
