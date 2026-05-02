<div align="left">

<div align="center">
<kbd>
  <br>
  <h1> L E A R N I N G _ N E T W O R K S </h1>
  <br>
</kbd>

<br>

<br>

<div align="center">
  <img src="https://img.shields.io/badge/[_NETWORK_]-_ADMIN_-00FF41?style=for-the-badge&labelColor=black" alt="Network Admin">
  <img src="https://img.shields.io/badge/[_TCP/IP_MODEL_]-_LAYERS_1--5_-00FF41?style=for-the-badge&labelColor=black" alt="TCP/IP">
  <img src="https://img.shields.io/badge/[_PACKET_]-_CAPTURED_-00FF41?style=for-the-badge&labelColor=black" alt="Packets">
</div>
</div>

<br>

<hr>

## Sobre o Repositório

Repositório para registros de tráfego e infraestrutura prática desenvolvida no **4º semestre da graduação**. Aqui, os protocolos deixam de ser teoria e se tornam implementações reais de rede.


### Camadas de Abstração (TCP/IP Model)
* **[L5] Aplicação:** Interface direta com o usuário e serviços de rede (HTTP, DNS, FTP, DHCP).
* **[L4] Transporte:** Controle de fluxos `TCP/UDP` e mecanismos de janela.
* **[L3] Rede:** Roteamento, máscaras de sub-rede e endereçamento `IPv4/IPv6`.
* **[L2] Enlace:** Frames, switches e controle de acesso ao meio (`MAC`).
* **[L1] Física:** Transmissão de sinais e infraestrutura de hardware.

### Toolset do Operador

> `Wireshark` -> Inspeção profunda de pacotes (Deep Packet Inspection).
> `Cisco Packet Tracer` -> Modelagem de infraestruturas críticas.
> `Socket Programming` -> Implementação de canais de comunicação em baixo nível.
> `Nmap` -> Auditoria de rede e mapeamento de nós ativos.

## Estrutura do Sistema

```bash
root@networks:~/LearningNetworks$ tree
.
├──  camada-aplicacao/    # HTTP, DNS, DHCP, FTP
├──  camada-transporte/   # Handshake TCP, Portas UDP
├──  enderecamento-ip/    # Calculadoras de Sub-rede e VLSM
├──  simulacoes-packet/   # Arquivos .pkt (Topologias Cisco)
└──  socket-lab/          # Comunicação Client-Server
