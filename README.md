# PySync CLI 

O **PySync CLI** é uma ferramenta de linha de comando robusta para sincronização incremental de arquivos, desenvolvida em Python. Ideal para automação de backups e espelhamento de diretórios, o projeto foca em eficiência, segurança e auditabilidade.

---

## Funcionalidades

- **Sincronização Incremental:** Copia apenas arquivos novos ou modificados (baseado em metadados de tempo), economizando tempo e recursos.
- **Modo Simulação (`--dry-run`):** Permite visualizar todas as operações de cópia ou exclusão antes que elas ocorram de fato.
- **Modo Espelho (`--mirror`):** Remove arquivos no destino que não existem mais na origem, garantindo uma cópia idêntica.
- **Audit Log com SQLite:** Todas as execuções, sucessos e erros são registrados em um banco de dados local para consultas futuras.
- **Arquitetura Modular:** Código separado em motor de sincronização, persistência de dados e interface CLI.

---

## Tecnologias Utilizadas

- **Python 3.x**
- **SQLite3** (Persistência de dados)
- **Argparse** (Interface de linha de comando)
- **OS/Shutil** (Manipulação de sistema de arquivos)

---

## Como Usar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado em sua máquina Linux.

### Instalação
Clone o repositório:
```bash
git clone [https://github.com/SEU_USUARIO/pysync-cli.git](https://github.com/SEU_USUARIO/pysync-cli.git)
cd pysync-cli
