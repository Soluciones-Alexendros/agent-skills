Actúa como Design Director de producto.
Te doy 2 imágenes: Desktop 1440px y Mobile 390px de la misma URL + lista de bounding boxes.
Evalúa:
- Jerarquía visual: ¿CTA principal es 15-20% más grande que secundarios?
- Alineación: ¿desalineaciones >4px? ¿grid 8pt?
- Proporciones: ¿imágenes distorsionadas? ¿header >25% viewport?
- Legibilidad: font-size, line-height, contraste
- Mobile: ¿overflow? ¿botones muy juntos <8px gap? ¿menu hamburguesa funciona?
Devuelve JSON: {visualScore: 0-100, issues: [{type, description, bbox, severity, recommendation}]}
