// Função para obter os blocos da blockchain
function getBlocks() {
    fetch('http://localhost:5000/blocks')
        .then(response => response.json())
        .then(data => {
            document.getElementById('blocks').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Erro ao obter os blocos:', error);
        });
}

// Função para registrar um novo bloco
function registerBlock() {
    const blockData = document.getElementById('blockData').value;
    if (!blockData) {
        alert('Por favor, insira os dados do bloco.');
        return;
    }

    fetch('http://localhost:5000/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ data: blockData })
    })
    .then(response => response.json())
    .then(data => {
        alert('Bloco registrado com sucesso!');
        document.getElementById('blockData').value = ''; // Limpar o campo de input
    })
    .catch(error => {
        console.error('Erro ao registrar o bloco:', error);
    });
}

// Função para auditar a blockchain
function auditChain() {
    fetch('http://localhost:5000/audit')
        .then(response => response.json())
        .then(data => {
            document.getElementById('auditResult').textContent = JSON.stringify(data, null, 2);
        })
        .catch(error => {
            console.error('Erro ao auditar a blockchain:', error);
        });
}

// Função para sincronizar a blockchain com os peers
function synchronizeChain() {
    fetch('http://localhost:5000/synchronize')
        .then(response => response.json())
        .then(data => {
            alert('Blockchain sincronizada com sucesso!');
        })
        .catch(error => {
            console.error('Erro ao sincronizar a blockchain:', error);
        });
}

// Função para registrar um novo peer
function registerPeer() {
    const peerAddress = document.getElementById('peerAddress').value;
    if (!peerAddress) {
        alert('Por favor, insira o endereço do peer.');
        return;
    }

    fetch('http://localhost:5000/register_peer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ peer: peerAddress })
    })
    .then(response => response.json())
    .then(data => {
        alert('Peer registrado com sucesso!');
        document.getElementById('peerAddress').value = ''; // Limpar o campo de input
    })
    .catch(error => {
        console.error('Erro ao registrar o peer:', error);
    });
}
