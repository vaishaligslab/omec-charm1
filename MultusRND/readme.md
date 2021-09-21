**Network_Attachment_Definition**

This code is used to create custom network resource as per ovs-network.yaml.

```
python3 ovs-network_test.py
```

Error while excuting above code is as below 

```
Traceback (most recent call last):
  File "onetest.py", line 5, in <module>
    utils.create_from_yaml(k8s_client, yaml_file)
  File "/home/vagrant/.local/lib/python3.8/site-packages/kubernetes/utils/create_from_yaml.py", line 92, in create_from_yaml
    return create_with(yml_document_all)
  File "/home/vagrant/.local/lib/python3.8/site-packages/kubernetes/utils/create_from_yaml.py", line 76, in create_with
    created = create_from_dict(k8s_client, yml_document, verbose,
  File "/home/vagrant/.local/lib/python3.8/site-packages/kubernetes/utils/create_from_yaml.py", line 146, in create_from_dict
    created = create_from_yaml_single_item(
  File "/home/vagrant/.local/lib/python3.8/site-packages/kubernetes/utils/create_from_yaml.py", line 172, in create_from_yaml_single_item
    k8s_api = getattr(client, fcn_to_call)(k8s_client)
AttributeError: module 'kubernetes.client' has no attribute 'K8sCniCncfIoV1Api'

```
