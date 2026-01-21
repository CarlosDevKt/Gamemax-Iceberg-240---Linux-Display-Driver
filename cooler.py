import usb.core
import usb.util
import psutil
import time
import sys

# IDs do hardware Gamemax
VENDOR_ID = 0x5131
PRODUCT_ID = 0x2007
    
def get_stats():
    """Captura temperatura, uso de CPU e especificamente o FAN 2."""
    # 1. Temperatura
    temp = 0
    temps = psutil.sensors_temperatures()
    for name in temps:
        for entry in temps[name]:
            if entry.current > 0:
                temp = int(entry.current)
                break
        if temp > 0: break

    # 2. Porcentagem da CPU (Garante que seja INTEIRO)
    cpu_usage = int(round(psutil.cpu_percent(interval=None)))

    # 3. RPM do FAN 2
    rpm = 0
    fans = psutil.sensors_fans()
    for name in fans:
        entry_list = fans[name]
        if len(entry_list) >= 2:
            # Pegamos o segundo item (índice 1 é o Fan 2)
            rpm = int(entry_list[1].current)
            break
    
    return temp, cpu_usage, rpm

def setup_device():
    dev = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)
    if dev is None:
        print("Erro: Water Cooler Iceberg 240 não encontrado!")
        sys.exit(1)

    for config in dev:
        for i in range(config.bNumInterfaces):
            try:
                if dev.is_kernel_driver_active(i):
                    dev.detach_kernel_driver(i)
            except Exception:
                pass

    try:
        dev.set_configuration()
    except usb.core.USBError as e:
        print(f"Erro ao configurar: {e}")
        sys.exit(1)

    cfg = dev.get_active_configuration()
    intf = cfg[(0, 0)]
    ep_out = usb.util.find_descriptor(
        intf,
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
    )
    return dev, ep_out.bEndpointAddress

def send_update(dev, endpoint, temp, cpu, rpm):
    data = [0] * 64
    data[0] = 1                # Report ID
    data[1] = int(temp)        # Temperatura
    data[2] = int(cpu)         # Uso de CPU
    
    # --- VARIAÇÃO A (RPM em 2 bytes: High e Low) ---
    # Se o RPM for 1500:
    # High Byte (data[3]) = 1500 // 256 = 5
    # Low Byte  (data[4]) = 1500 % 256  = 220
    data[3] = int(rpm >> 8) & 0xFF  # Byte Mais Significativo
    data[4] = int(rpm & 0xFF)       # Byte Menos Significativo

    try:
        dev.write(endpoint, bytearray(data), timeout=1000)
    except usb.core.USBError as e:
        print(f"\nErro USB: {e}")

def main():
    print("--- Driver Gamemax Iceberg Ativo (Python 3.14+) ---")
    device, addr = setup_device()

    # Inicializa o contador de CPU
    psutil.cpu_percent(interval=None)

    try:
        while True:
            temp, cpu, rpm = get_stats()
            print(f"\r[INFO] Temp: {temp}°C | CPU: {cpu}% | Fan2: {rpm} RPM    ", end="")
            send_update(device, addr, temp, cpu, rpm)
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nEncerrando driver...")
    finally:
        usb.util.dispose_resources(device)

if __name__ == "__main__":
    main()
