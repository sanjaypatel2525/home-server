# Home-Server 
This is a google photos alternative. So why do I need this.
1. Cost
2. Local content(photos/media/files) backup server
3. Built on docker, no code just run ``docker-compose up``.
5. Optional - backup your data to any cloud provider such as s3 deep archive.
4. Optional - Local solid media server JellyFin that supports Andorid, IOS, Web Browser. 
6. Optional - Face/Object detection, search etc using Libre Photos  
7. Optional - Wireguard VPN, allows you to saftely access your media from anywhere.

## Stack used
1. [Docker](https://www.docker.com/) - Open source framework to run containers.
2. [Resilio](https://www.resilio.com/) - Free sync from phone to your local server.
3. [Duplicati](https://www.duplicati.com/) - Redundancy free open source incremental backup of your local server data to another local storage. 
4. [Jellyfin](https://jellyfin.org/) - Free open source local media server.
4. [LibrePhotos](https://docs.librephotos.com/) - Free open source ML based face/object/location detection, Web browser app. 
4. [Wiredguard](https://www.wireguard.com/) - Free open source VPN
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
9. Optional(Not recommended) - Spin up wireguard VPN container to access to your media from anywhere. 

## More technical stuff.
### High level data diagram.
![homeserver1 drawio](https://github.com/sanjaypatel2525/home-server/assets/8791115/0c2a7f6c-2982-4a29-9a1a-8604164527c4)
[Edit](https://viewer.diagrams.net/?tags=%7B%7D&highlight=0000ff&edit=_blank&layers=1&nav=1#R7Vtbc5s4FP41nuk%2BxAOI62PiJO22STaznm7afdmRjWzUYESFHNv59SsZYQNSYjcGu67bhxQOSMD5zvnORXIH9Cbz9xSm0S0JUdyxjHDeAZcdyzIDw%2BD%2FCclCSlxg55IxxaGUrQV9%2FIykUA4cT3GIssqNjJCY4bQqHJIkQUNWkUFKyax624jE1aemcIwUQX8IY1X6gEMW5VLfMdbyDwiPo%2BLJZvHFE1jcLAVZBEMyK4nAVQf0KCEsP5rMeygW2iv0ko%2B7fuHq6sUoStg2A749fP7X8r7defTT3b15DePLT5%2FOHDnNE4yn8ovl27JFoQJKpkmIxCxmB1zMIsxQP4VDcXXGUeeyiE1ieVl9q%2BIJiDI0L4nkW75HZIIYXfBb5NWzQrnSZs7MQjBbI%2BC5UhaVtO8CKYQS9fFq8rVi%2BIHUzQ%2FoybYb1tMIx3GPxIQux4JRMPLE0IuMUfKISleACwIQNqNZS9GspWrW1mnWcdrSrBVs1iwKuU%2FKU0JZRMYkgfHVWnqx1r3Bz9b33BCSSo1%2FQ4wtJMHAKSNVPLhS6eKLGN%2B1A7sQfBVXu4YNCsHlXD4iP1uUz%2B4RxVwniErhi4BlZEqH6DWduJLpIB0j9sqNBUsKBb1qABTFkOGnKqnpsJRD7wnmL70yHACMruFw%2FzIdzw9sz6mYEbBrxpG%2Ft5yjZh%2Brl3q7yXiHNZCycRhdZ4Np7GAFWxqB27QN7ObPm925pFXBXZhH2xs4QPE9yTDDJOHXBoQxMuE3wBiPhWDI1Sc86yIWd17A4eN4CWmZQ5f%2FSpOey7FMQCyZtQjilo5rDcM3rgVoq1gtTkKYRSvL4VdS8RmT%2BVhkPF1MMq%2BLefaRdbMJpCyNSIKaYWvbrHhZoFK16atM3VoIBAqwf%2BYfaxnv%2FkYZjjHhh%2Bdp%2BocCOP9gVvUmBdY6ZhMchrnj8qmf4WA5lQAgFayy%2FDbnouNcirm4r2a525oKqkkORzncFiKSsIIzNMnUj6ctZpUVTaABDGhiq9UWYsFp8KR9lDy5RUL5myffwpOmd2CidBRkz5OQEj7mN1PmTGlVy5BVsV9GzN4nU664Zq9U%2BXbKO1x9sJOaXcUz1u7Q40YGccJN3DL6iD6JgyYLbBh6cKgjs4HtOobdUIHtVS3b1Fm2petctGXZpntMSQCaY%2FalmIMf56OA5cvz9TBxUh7VXPFdQLbZuZymnUtffNtGjS7rxpJ%2FUmvlNtC47TTJxJdzzxAfOOG%2BG2ntbJmvtBfQVJRfdQLFkVd9Y%2FmUTrk1qw1dRte1g6CCR9GP2BHmVW1Q1HugOgMZjTLUCsCFxZ9iLsoIXa4ANML%2BQc1RNX1rX0P%2BQBBjS%2FSv9vdvCFezAFcGWaMvdWC5scg9B1zmjsWRmbFlYE4Xp5mnglo0t3SVha6ib620MLforgktVPzDdXu9Fz1sozPHtQsrfBXAS8ZApizmuVxvtShnqBlZb%2FlP59Ku75sXouXO3TXEaP05EudCfIkpnz1%2FrURkKXrGqHl%2FgtiM0Mesy00YUZ7V%2FNcoCawWporooFli0ZGA35rNqI27K%2FnlZec%2FRQe3%2FWrLTtdiNfdZh9qHWdrQZt3O6zn3er3MsKpJfuBvyvKbXS0r8vDNCbvVdMK%2Bm2OqjaLLaRpzl2L4VymIbf9nK4iLiFnS%2Bq0oX2Lx1n8lQ7GeMaQIMiQqHDUp4lbGn%2FuMU%2F4XJUO6SBkSnT37PdeXMYjJ8DE7DjZtAF63Vpqudr%2BU4fX2mSFZal%2B9v0iGAstZhBLxqmTK%2F5J0eQLT9GTAMkE12vkarHR7P9rruqoE2IvJNFSdDtDwpUqEPwenGSolesPlHD%2FKhwMzDEeGjg9NwwNBU9mhXXUYoFsk1PFha%2Bmh5SsgHCIHeXv433qzjNV4v243xatttRucTOd5U6oI%2FUcX8est8NXmoINFfKCGhHvI%2BXtZ%2F1xCBvmsw9NrcrzSpNpz0eMfF%2BEAf0vCKSrvn4RwgMr0H%2FmwxTVOauXGLQoxPOayA9TKjjNdrrNXErIPsxlHVvbrav5r6Yq%2Bsn%2B7YxRM3%2FaCmFNLooIaaC1vPy2eXgncA4ruI8IZvepK9UT29qaz3PlxhD7l%2FHQ%2BBdRSXtfZrGNgJS8WE792xC9qkFqGplvV0CUA7f24QpMJy0WqFyLQSeBk1R1O1zwL9pmpOarDfeBTc4lcVOGzPuARPk28zpwaXNvW9k3g9f0z%2Bh59vhncOeHX5%2BRjFJqwf6Yu%2Fj5gisZTuGyn%2FHN%2FV8v73v2ViuU0GKsbE%2FcSnzT7MxREto5P1rbqbyI%2BadUPDpHyaVOwjfmc9v2lt5frnJfNbA9VzWsveYp7V9R91Ds5kBdUN1JbtqM6UEsbqbXQqn2b80S8b4ie8HKdZobFtrN6flfmuF4sNgocbTzaDc9amWR5TleDqI4S6z%2Fo2wJSfrr%2BLXNeaq1%2FEg6u%2Fgc%3D)

### Security
Please use this at your own risk. Current setup runs on your local server local network. Connection to this host can only be made from you local network. Tighten up router security to secure your network if needed.  

### Can I use it from outside network or internet. 
Sure you can setup port forwarding on you router and forward that to wireguard container port 51820. Opening any port to internet is always risky, It comes with security concerns and you would have to tighten up that security. Wireguard is top class fast open source vpn that uses private public key encryption. You can download wireguard vpn on your mobile/laptop to connect to your home network. Wireguard requires a static ip to work, you can either choose to by static ip for your machine or use dynamic dns services for ex: duckdns.org many more (Feel free to choose any). Your home router has a public Ip, it keeps rotating every so often. You can ``curl ifconfig.me`` to get you public ip. This stack include linux crontab that update your public ip to your dyanmic dns service. You can use this dns name for wireguard configuration. 

### Why external drive and three copies.
External drive helps to keep the data redundant locally. Downloading data back from Cloud can be costly and external drive can save you this cost. 

### How to restore data back?
1. If you have data on external storage, you follow [Duplicati](https://duplicati.readthedocs.io/en/latest/08-disaster-recovery/) restore guidelines.
2. If you lost data locally, download cloud storage (S3 Deep archive) guarantees to provide you data back withing 12hrs. Then follow Duplicati restore process.

### When can we see gcloud, azure and other cloud support? 
Currently there is no plan, but it's pretty easy to develop such feature in python. 
