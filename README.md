# ❄️ Gamemax Iceberg 240 – Linux Display Driver 🐧

Este projeto é um driver em **Python** desenvolvido para controlar o display LCD do water cooler  
**Gamemax Iceberg 240** no Linux.

Ele permite monitorar e exibir em tempo real:

- 🌡️ Temperatura da CPU  
- 📊 Uso da CPU (%)  
- 🌀 Rotação das ventoinhas (RPM)

---

## 🚀 Funcionalidades

- Monitoramento de CPU em tempo real
- Leitura de temperatura (Intel / AMD)
- Leitura de RPM do FAN 2
- Compatível com **Python 3.14+**
- Testado no **Fedora 43**

---

## 🛠️ Pré-requisitos

### 🟦 Fedora / Nobara
~~~bash
sudo dnf install python3-pip libusb1 lm_sensors -y
pip install psutil pyusb
~~~

### 🟧 Ubuntu / Debian / Mint
~~~bash
sudo apt update && sudo apt install python3-pip python3-usb libusb-1.0-0 lm-sensors -y
pip install psutil pyusb --break-system-packages
~~~

---

## ⚙️ Configuração Crítica de Hardware

⚠️ Siga a seção 1️⃣ **apenas se**:
- RPM aparecer como `0`
- Temperatura aparecer zerada
- O dispositivo USB não for detectado

---

### 1️⃣ Correção de Conflito ACPI (Kernel)

Edite o GRUB:
~~~bash
sudo nano /etc/default/grub
~~~

Adicione dentro de `GRUB_CMDLINE_LINUX_DEFAULT`:
~~~text
acpi_enforce_resources=lax
~~~

Atualize o GRUB:

**Ubuntu / Debian**
~~~bash
sudo update-grub
~~~

**Fedora / Arch**
~~~bash
sudo grub-mkconfig -o /boot/grub/grub.cfg
~~~

➡️ Reinicie o sistema.

---

### 2️⃣ Ativação dos Sensores
~~~bash
sudo sensors-detect --auto
~~~

---

### 3️⃣ Permissões USB (udev)
~~~bash
echo 'SUBSYSTEM=="usb", ATTR{idVendor}=="5131", ATTR{idProduct}=="2007", MODE="0666"' | sudo tee /etc/udev/rules.d/99-gamemax.rules
sudo udevadm control --reload-rules && sudo udevadm trigger
~~~

---

## 💻 Como Executar
~~~bash
python3 cooler.py
~~~

---

## 📌 Observações

- Verifique se o dispositivo aparece em `lsusb`
- Não é necessário rodar como root após configurar o udev
- Secure Boot pode bloquear sensores

---

## 📄 Licença

MIT License
