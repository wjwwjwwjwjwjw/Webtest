// ģ�����ݴ洢
let items = [
  { id: 1, name: '��ĿA' },
  { id: 2, name: '��ĿB' },
  { id: 3, name: '��ĿC' }
];

export default function handler(req, res) {
  // ��ȡ������Ŀ
  if (req.method === 'GET') {
    return res.status(200).json(items);
  }
  
  // �������Ŀ
  else if (req.method === 'POST') {
    const newItem = {
      id: Date.now(), // ʹ��ʱ�����Ϊ��ʱID
      name: req.body.name
    };
    
    items.push(newItem);
    return res.status(201).json(newItem);
  }
  
  // ɾ����Ŀ
  else if (req.method === 'DELETE') {
    const id = parseInt(req.query.id);
    const itemIndex = items.findIndex(item => item.id === id);
    
    if (itemIndex !== -1) {
      const deletedItem = items[itemIndex];
      items = items.filter(item => item.id !== id);
      return res.status(200).json(deletedItem);
    } else {
      return res.status(404).json({ message: '��Ŀδ�ҵ�' });
    }
  }
  
  // ��֧�ֵķ���
  else {
    res.setHeader('Allow', ['GET', 'POST', 'DELETE']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
} 