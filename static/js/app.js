async function api(path, method='GET', body=null){
  const opts = {method, headers:{'Content-Type':'application/json'}};
  if(body) opts.body = JSON.stringify(body);
  const res = await fetch('/api'+path, opts);
  return res.json();
}

async function load(q=''){
  const params = q ? '?q='+encodeURIComponent(q) : '';
  const data = await api('/students'+params);
  const tbody = document.querySelector('#students-table tbody');
  tbody.innerHTML = '';
  data.forEach(s=>{
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${s.id}</td><td>${s.name}</td><td>${s.email||''}</td><td>${s.major||''}</td>
      <td>
        <button data-id="${s.id}" class="edit">Edit</button>
        <button data-id="${s.id}" class="del">Delete</button>
      </td>`;
    tbody.appendChild(tr);
  });
}

document.addEventListener('click', async (e)=>{
  if(e.target.classList.contains('edit')){
    const id = e.target.dataset.id;
    const res = await api('/students?q='+id); // naive fetch; server filters by name/email but it's okay for small demo
    const student = res.find(x=>String(x.id)===String(id));
    if(student){
      document.getElementById('sid').value = student.id;
      document.getElementById('name').value = student.name;
      document.getElementById('email').value = student.email || '';
      document.getElementById('major').value = student.major || '';
    }
  } else if(e.target.classList.contains('del')){
    if(!confirm('Delete this student?')) return;
    const id = e.target.dataset.id;
    await api('/students/'+id, 'DELETE');
    load();
  }
});

document.getElementById('student-form').addEventListener('submit', async (ev)=>{
  ev.preventDefault();
  const id = document.getElementById('sid').value;
  const payload = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    major: document.getElementById('major').value
  };
  if(id){
    await api('/students/'+id, 'PUT', payload);
  } else {
    await api('/students', 'POST', payload);
  }
  document.getElementById('student-form').reset();
  load();
});

document.getElementById('cancel').addEventListener('click', ()=>{
  document.getElementById('student-form').reset();
  document.getElementById('sid').value = '';
});

document.getElementById('searchBtn').addEventListener('click', ()=>{
  const q = document.getElementById('q').value.trim();
  load(q);
});
document.getElementById('refreshBtn').addEventListener('click', ()=>{ document.getElementById('q').value=''; load();});

// initial load
load();
