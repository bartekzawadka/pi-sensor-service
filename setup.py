import os
import shutil
from distutils.core import setup
from distutils.command.install import install


class PostInstall(install):
    def run(self):
        install.run(self)

        if not os.path.exists('/etc/pi-sensor-service/config'):
            print "Copying config file"
            directory = '/etc/pi-sensor-service/'
            if not os.path.exists(directory):
                os.makedirs(directory)

            config_path = os.path.join(os.getcwd(), "config")
            shutil.copyfile(config_path, os.path.join(directory, "config"))
        else:
            print "Config file already exists"

        if not os.path.exists('/etc/init.d/pi-sensor-service'):
            print "Adding init.d script"

            shutil.copyfile(os.path.join(os.getcwd(), "scripts", "pi-sensor-service"), "/etc/init.d/pi-sensor-service")
            os.system("chmod 755 /etc/init.d/pi-sensor-service")
        else:
            print "Init.d script already exists"


setup(name='pi-sensor-service',
      version='1.0',
      description='Raspberry Pi DHT21 sensor (temp and humidity) data REST service',
      author='Bartek Zawadka',
      author_email='kontakt@bartoszzawadka.pl',
      packages=['pi-sensor-service'],
      cmdclass={'install': PostInstall})
