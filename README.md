# Home-Server 
This is a google photos alternative. So why do I need this.
1. Cost
2. Local content(photos/media/files) backup server
3. Built on docker, no code just run ``docker-compose up``.
5. Optional - backup your data to any cloud provider such as s3 deep archive.
4. Optional - Local solid media server JellyFin that supports Andorid, IOS, Web Browser. 
6. Optional - Face/Object detection, search etc using Libre Photos  

## Stack used
1. [Docker](https://www.docker.com/) - Open source framework to run containers.
2. [Resilio](https://www.resilio.com/) - Free sync from phone to your local server.
3. [Duplicati](https://www.duplicati.com/) - Redundancy free open source incremental backup of your local server data to another local storage. 
4. [Jellyfin](https://jellyfin.org/) - Free open source local media server.
4. [LibrePhotos](https://docs.librephotos.com/) - Free open source ML based face/object/location detection, Web browser app. 
4. Python Scripts - Uploads your backup to cloud such as s3 deep archive. 

## How to run
1. Checkout repo
2. Update all environment(.env) files.
3. Start all container
4. Install Resilio mobile app, setup Resilio and connect it to you local server Resilio endpoint.
5. Start Resilio backup. 
6. Optional (Highly recommended) - Setup Duplicati backup for redundant backup to another drive/media.
    1. Go to \<localserver_ip>:8200
    2. Add backups
    3. Give any name ('home-server)
    4. **Very Important** - Create encryption password and store it in place where you don't forget.
    5. Select local folder or drive '/source'. '/source' is mapped in .env file.
    6. Select schedule (Tip - use monthly backups, it would create less files and will save cost with Cloud if you are using any).
    7. Optionally run the backup after Resilio backup is finished.
7. Optional (Recommended) - Enable cloud backup. In extreme cases when you lost all your data from local server and also from second pair of storage(Above), this comes to resuce.  
    1. We have used s3 Glacier deep archive which [costs](https://calculator.aws/#/estimate) around $1 per 100GB per year compared to $20 Google and $18 ICloud. 
    2. It's 99.999999999% durable.
    3. You can use prepaid card with this service to make sure there are no surprise charges.
    4. How to enable.
        1. Create file ~/.aws/credential and add credential under profile name 'home-server', you can get these credential from cloud provider.
        2. Optional - Make sure these credential have only s3 read write access. More downscoped access better.
        3. Start the container. Current crontab is scheduled to run once a month.
8. Optional(Not recommended) - You can start LibrePhoto container to get browser based app that uses ML on Photos. It not recommeded becuase it requires desktop grade PCs and even with that browser based app not very responsive. It may be good for small set of data but with 100GB of data is slogs. 

## More technical stuff.
### High level data diagram.
![download](https://github.com/sanjaypatel2525/home-server/assets/8791115/6d048a8e-9546-4aa3-9920-40820ea23dfa)
[Edit](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1&title=1.xml#R7Vtbc5s4FP41ntl9iAcQ18faTtrdJt3MZnba7suODLKtBiNGyLWdX78SiLtspzXYdd08JHBAQpzvnO9cRAZgvNy8pTBePJAAhQNDCzYDMBkYhmGaDv8jJNtMonu6kUnmFAdSVgqe8AuSQk1KVzhASe1GRkjIcFwX%2BiSKkM9qMkgpWddvm5Gw%2FtQYzlFL8OTDsC39iAO2yKSupZXydwjPF%2FmTdU1eWcL8ZilIFjAg64oI3A7AmBLCsqPlZoxCob1cL9m4ux1Xi4VRFLHXDPjy8Z9%2FDefLB4e%2B%2F%2FCo38Fw8v79jSWn%2BQrDlXxjuVq2zVVAySoKkJhFH4DReoEZeoqhL66uOepctmDLUF6W0yHK0GbnQvXi9bnhILJEjG75LXLATa5caTM3ei5Ylwg4tpQtKtq3gRRCifq8mLxUDD%2BQuvkGPZlmx3qa4TAck5DQdCyYeTNHDB0ljJJnVLkCbOCBoBvNGi3NGm3NmirNWlZfmjW8w5pFAfdJeUooW5A5iWB4W0pHpe41flbec09ILDX%2BBTG2lQQDV4zU8eAapNtPYvzQ9Mxc8FlcHWomyAWTjXxEdratnj0iirlOEJXC7DXE2vfDxV%2BVrKiP9inJltQH6RyxPTfqmtoAKAohw1%2FrK1FhKYc%2BEszXWBgOANpQs7h%2F6ZbjeqZj1cwImA3jyJYp52jYR7Go7zcZ57wGUjUObWgdMI0ureCVRmAfaQPH%2BfNhd65oVdAZ5tH2Hk5R%2BEgSzDCJ%2BLUpYYws%2BQ0wxHMh8Lm2hGeNQnHnCPrP8xTSKoemP5VJ38ixTEAsmTUP4oaKazXN1e4EaEWsFicBTBaF5fArsXiN5WYuMp4hJokzxDz7SIbJElIWL0iEumFrU695mdemat1tM3VvIRC0gP0je1lD%2B%2B1vlOAQE374Jo5%2FbwHOdcDq3tSCtYnZEgdB5rh86hc4TacSAMSCVdJ3s0YDayLm4r6aZG6rt1CNMjiq4TYXkYjlnKF3ABdPU2p46UABGFDEVqMvxLwr5UnzEnjyFQnlL578Hp7UnTMTpdVC9k0UUMLH%2FGLKjCmNehlSFPtVxMxTMmVBLSelyg4p72T1wVFqtlueUbrDmBsZxBE3cUN7QvSrOOiywIaBA30VmU1N29LMjgpsp27ZusqyDVXnoi%2FL1u1LSgLQBrNP%2BRz8OBsFDFeel8PESXVUj8V3juFh57KOdC518W1qDbpsGkv2Br2V20DhtqsoEerlziJecMl9d6G0szRf6S%2Bg7XRZ2Q6WgwdF5Kjiv8dfdocubWibnlfDI%2B9HHAlzURvk9R6oz0BmswT1AnBu4NeYizJC0x2ATtjfaziqom%2FtKsgfCGLsif7b%2Ff17wtUswJVBVnuSOjDsUOSeUy6z5%2BJIT1gamOPtdeapoBHNDVVloaroeyst8s2zfZ4qtFDzD9sej3d62EFnDhsXCnxbgFeMgaxYyHO5cbEpp7UzsnH6o3Jp23X1kWi5c3cNMCpfR%2BKciyeY8tmzZUUiS1EzRsP7I8TWhD4nQ27CiPKs5r9OSaDYmMqjg2KLRUUCbm82027c3co3rzr%2FNTq46dZbdqoWq37KOtQ8z9aGMuu29ufc5X6ZZtSTfM89lOX3vFuWN2IPJ%2BzGkQn7cY7ZbhRNVnHIXYrhn6UgNt0frSDOI2ZF6w%2BifAnFqv%2BKfLGf4VMEGRIVTjsp4kbFn%2FuCY%2F4bRT7dxgyJzp75lutLm4bEf04ug007gNdulKbF1y9VeJ1TZkhGu6%2F%2BtI18geV6gSKxVLLiv0mcnsA4vhqwdFCPdq4CK9W3H%2F11XdsEOA7JKmg7HaDBrkqEPwfHCaoken46x7fy4VQPgpmm4kNdc4DXVXZo1h0GqDYJVXzYW3pouC0QzpGDdBj%2BX%2F2xjHFsv%2B44xbfbavc4Wm2y7lUe%2Bi8u4jdb4MXHQWeL%2BKAdEh4h5%2B%2B0%2FplABvms%2FvU1OfY0qU5c9LgXTjjAfSXhZKX4uQgHtJn%2BTz5se4ejRrnxgAIML7nsAI2y40aV65yUhMzzfIwjK%2Fuymv9cuaKu7Dt0DLOfr1GtRhLlNUDr%2BfPT%2FOm1wD2l6HFBOKPXXamZyD7cD9IvPy7Qp6wfzqdAu5RXdTabGBjRzmLi5474eQ3SyNBUuxqqBKC%2Ff65QZMJyk2pHBLoKnIymw6maZ94pMzWr7XDv%2BNRcIjdV%2BKwf8QxfJ143VgOu19b234EXPy3%2FcywLbOU%2F4IHb%2FwE%3D)

### Security
Please use this at your own risk. Current setup runs on your local server local network. Connection to this host can only be made from you local network. Tighten up router security to secure your network if needed.  

### Can I use it from outside network or internet. 
Sure you can setup port forwarding on you router and can access your local machine, it comes with security concerns and you would have to tighten up that security. 

### Why external drive and three copies.
External drive helps to keep the data redundant locally. Downloading data back from Cloud can be costly and external drive can save you this cost. 

### How to restore data back?
1. If you have data on external storage, you follow [Duplicati](https://duplicati.readthedocs.io/en/latest/08-disaster-recovery/) restore guidelines.
2. If you lost data locally, download cloud storage (S3 Deep archive) guarantees to provide you data back withing 12hrs. Then follow Duplicati restore process.

### When can we see gcloud, azure and other cloud support? 
Currently there is no plan, but it's pretty easy to develop such feature in python. 