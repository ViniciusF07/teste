const formTarefa = document.querySelector('#form-tarefa');
const listaTarefas = document.querySelector('#lista-tarefas');

formTarefa.addEventListener('submit', (event) => {
  event.preventDefault();

  const descricao = document.querySelector('#descricao').value;
  const responsavel = document.querySelector('#responsavel').value;
  const nivel = parseInt(document.querySelector('#nivel').value);
  const prioridade = parseInt(document.querySelector('#prioridade').value);

  fetch('https://teste-production-9ef9.up.railway.app/criartarefas', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      descricao,
      responsavel,
      nivel,
      prioridade,
    }),
  })
    .then((response) => response.json())
    .then((tarefa) => {
      const li = document.createElement('li');
      li.innerHTML = `${tarefa.descricao} - ${tarefa.responsavel} - ${tarefa.nivel} - ${tarefa.prioridade}`;
      listaTarefas.appendChild(li);
      formTarefa.reset();
    });
});

fetch('/tarefas')
  .then((response) => response.json())
  .then((tarefas) => {
    tarefas.forEach((tarefa) => {
      const li = document.createElement('li');
      li.innerHTML = `${tarefa.descricao} - ${tarefa.responsavel} - ${tarefa.nivel} - ${tarefa.prioridade}`;
      listaTarefas.appendChild(li);
    });
  });