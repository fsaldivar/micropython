# micropython

Debes tener un NODE MCU

Borrar Micropython

C:\Users\f_sal\Anaconda3\Lib\site-packages>python esptool.py --port COM29 erase_flash

Instalar Micropython, hay que estaer en modo boot
C:\Users\f_sal\Anaconda3\Lib\site-packages>python esptool.py --chip esp32 --port COM29 write_flash -z 0x1000 esp32-idf3-20191220-v1.12.bin

usar uPyCraft para cargar los archivos de python.
