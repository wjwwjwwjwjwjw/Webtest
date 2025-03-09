// 模拟数据存储
let items = [
  { id: 1, name: '项目A' },
  { id: 2, name: '项目B' },
  { id: 3, name: '项目C' }
];

export default function handler(req, res) {
  // 获取所有项目
  if (req.method === 'GET') {
    return res.status(200).json(items);
  }
  
  // 添加新项目
  else if (req.method === 'POST') {
    const newItem = {
      id: Date.now(), // 使用时间戳作为临时ID
      name: req.body.name
    };
    
    items.push(newItem);
    return res.status(201).json(newItem);
  }
  
  // 删除项目
  else if (req.method === 'DELETE') {
    const id = parseInt(req.query.id);
    const itemIndex = items.findIndex(item => item.id === id);
    
    if (itemIndex !== -1) {
      const deletedItem = items[itemIndex];
      items = items.filter(item => item.id !== id);
      return res.status(200).json(deletedItem);
    } else {
      return res.status(404).json({ message: '项目未找到' });
    }
  }
  
  // 不支持的方法
  else {
    res.setHeader('Allow', ['GET', 'POST', 'DELETE']);
    return res.status(405).end(`Method ${req.method} Not Allowed`);
  }
} 