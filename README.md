# Обмен сообщениями с помощью ZeroMQ

**Рассматриваемые способы ZeroMQ взаимодействия**

* Push-Pull — push сокет (сервер) отправляет сообщения, а pull сокеты (клиенты) забирают или push сокеты (клиенты) отправляют на pull сокет (сервер).
* Request-Reply — req сокеты (клиенты) отправляют сообщения на rep сокет (сервер) и в ответ на каждое сообщение получают сообщение от rep сокета.
* Publish-Subscribe — pub сокет (сервер) отправляет сообщения на все sub сокеты (клиенты) или pub сокеты (клиенты) отправляют сообщения на sub сокет (сервер).

# Настройка окружения в lxc контейнере

```bash
lxc init ubuntu:18.04 blog-3
lxc config set blog-3 raw.idmap "both $UID 1000"
lxc config device add blog-3 project disk source=$PWD path=/home/ubuntu/blog-3
lxc start blog-3

lxc exec blog-3 -- sudo --login --user ubuntu
sudo cp blog-3/etc/.bashrc .
sudo chown ubuntu:ubuntu .bashrc
sudo cp blog-3/etc/.profile .
sudo chown ubuntu:ubuntu .profile
exit

lxc exec blog-3 -- sudo --login --user ubuntu
./bin/deps.sh

exit

lxc publish -f blog-3 --alias blog-3
```
