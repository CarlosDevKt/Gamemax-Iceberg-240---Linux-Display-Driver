# Gamemax Iceberg 240 - Linux Display Driver

Este projeto é um driver em Python desenvolvido para controlar o display LCD do Water Cooler **Gamemax Iceberg 240** no Linux. Ele permite monitorar e exibir em tempo real a temperatura da CPU, o uso de processador e a rotação das ventoinhas.

## 🚀 Funcionalidades
- **Monitoramento de CPU:** Uso percentual dinâmico.
- **Temperatura:** Leitura de sensores térmicos (Intel/AMD).
- **Fan RPM:** Captura específica do FAN 2 (ou configurável).
- **Compatibilidade:** Testado e funcional em **Python 3.14+** e Fedora 43.

## 🛠️ Pré-requisitos

Antes de rodar o script, você precisa instalar as bibliotecas necessárias!

Testado no Fedora 43, se você usa outra distribuição procure como instalar as bibliotecas abaixo:

```bash
sudo dnf install python3-pip libusb1 lm_sensors -y
pip install psutil pyusb
```

⚙️ Configuração Crítica de Hardware - Tente isso se não funcionar para você

    Parâmetro do Kernel: Edite o GRUB: sudo nano /etc/default/grub. Adicione acpi_enforce_resources=lax em GRUB_CMDLINE_LINUX_DEFAULT.

    Atualize e Reinicie:

        Ubuntu/Debian: 
        ```bash 
        sudo update-grub

        Fedora/Arch: 
        
        ```bash
        sudo grub-mkconfig -o /boot/grub/grub.cfg

        Reinicie o computador.

    Sensores: Execute
    ```bash
    sudo sensors-detect --auto.

    Permissões USB (udev):
    ```Bash
    echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="5131", ATTR{idProduct}=="2007", MODE="0666"' | sudo tee /etc/udev/rules.d/99-gamemax.rules
    sudo udevadm control --reload-rules && sudo udevadm trigger
```
💻 Como Executar
```bash

python3 cooler.py
