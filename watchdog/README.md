# Warchdog script

The plan is to intergrate this with huginn to generate alerts if there is a period of time where photos are not being written to the mobile backups folder.

For now the only function of this script is to POST a request to a webhook server when a file is written, it also comes with a systemd service that you can install and enable to ensure it is always running in case it crashes for whatever reason.

Install the service to `/etc/systemd/system/mobilePhotoBackupINotify.service`.

```none
sudo systemctl enable mobilePhotoBackupINotify.service
sudo systemctl start mobilePhotoBackupINotify.service
```

