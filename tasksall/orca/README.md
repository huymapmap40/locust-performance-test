# How to switch to locust 0.12.1 version?
```
cd locust
git apply tasks/orca/switch_locust_version.patch
```

# How to revert to current locust version?
```
cd locust
git apply -R tasks/orca/switch_locust_version.patch
```