"""Генерация BPMN 2.0 модели «Процесс управления логистикой» (ЛогиХаб, вариант 15).

Модель описывается декларативно (дорожки, элементы, потоки), а скрипт вычисляет
координаты и формирует XML с диаграммной частью (BPMN DI), совместимый с
bpmn.io / Camunda Modeler / draw.io.

    python bpmn/build_bpmn.py  ->  bpmn/logistics_process.bpmn
"""
from __future__ import annotations

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).with_name("logistics_process.bpmn")

POOL_X, POOL_Y, POOL_LABEL_W = 40, 40, 30
LANE_LABEL_W = 30
COL_W, FIRST_COL_X = 165, 150
ROW_H = 115

# id, название, число рядов
LANES = [
    ("Lane_Client", "Клиент (грузоотправитель)", 1.6),
    ("Lane_Manager", "Менеджер по логистике", 1.8),
    ("Lane_Warehouse", "Склад", 2),
    ("Lane_Dispatcher", "Диспетчер", 2),
    ("Lane_Driver", "Водитель", 1.25),
]

# id: (тип, название, дорожка, колонка, ряд)
NODES = {
    "Start": ("startEvent", "Возникла потребность в перевозке", "Lane_Client", 0, 0),
    "T_CreateOrder": ("userTask", "Оформить заявку на перевозку", "Lane_Client", 1, 0),
    "T_CheckOrder": ("userTask", "Проверить заявку", "Lane_Manager", 2, 0),
    "G_OrderOk": ("exclusiveGateway", "Заявка корректна?", "Lane_Manager", 3, 0),
    "T_Clarify": ("userTask", "Уточнить данные заявки", "Lane_Client", 3, 0),
    "T_Quote": ("serviceTask", "Рассчитать стоимость и срок доставки", "Lane_Manager", 4, 0),
    "T_Contract": ("userTask", "Сформировать договор-счёт", "Lane_Manager", 5, 0),
    "T_Pay": ("userTask", "Согласовать и оплатить счёт", "Lane_Client", 6, 0),
    "G_Paid": ("exclusiveGateway", "Оплата поступила в течение 3 дней?", "Lane_Manager", 7, 0),
    "End_Cancel": ("endEvent", "Заказ отменён", "Lane_Manager", 7, 1),
    "T_Pick": ("userTask", "Скомплектовать и промаркировать груз", "Lane_Warehouse", 8, 0),
    "G_Full": ("exclusiveGateway", "Груз укомплектован полностью?", "Lane_Warehouse", 9, 0),
    "T_Refill": ("userTask", "Докомплектовать груз", "Lane_Warehouse", 9, 1),
    "T_Waybill": ("userTask", "Оформить ТТН и передать груз к отгрузке", "Lane_Warehouse", 10, 0),
    "T_Route": ("serviceTask", "Построить маршрут и назначить транспорт", "Lane_Dispatcher", 11, 0),
    "T_Load": ("userTask", "Принять груз и начать рейс", "Lane_Driver", 12, 0),
    "T_Transport": ("userTask", "Выполнить перевозку", "Lane_Driver", 13, 0),
    "T_Replan": ("serviceTask", "Перепланировать маршрут и уведомить клиента", "Lane_Dispatcher", 13, 1),
    "End_Notified": ("endEvent", "Клиент уведомлён о новом ETA", "Lane_Dispatcher", 14, 1),
    "T_Deliver": ("userTask", "Доставить груз получателю", "Lane_Driver", 14, 0),
    "T_Accept": ("userTask", "Принять груз и проверить комплектность", "Lane_Client", 15, 0),
    "G_Remarks": ("exclusiveGateway", "Есть замечания?", "Lane_Client", 16, 0),
    "T_SignAct": ("userTask", "Подписать акт приёмки", "Lane_Client", 17, 0),
    "T_Claim": ("userTask", "Рассмотреть претензию и урегулировать", "Lane_Manager", 17, 0),
    "G_Merge": ("exclusiveGateway", "", "Lane_Manager", 18, 0),
    "T_Close": ("serviceTask", "Закрыть заказ и пересчитать OTIF", "Lane_Manager", 19, 0),
    "End_Done": ("endEvent", "Заказ выполнен", "Lane_Manager", 20, 0),
}

BOUNDARY = {"B_Delay": ("Отклонение от графика", "T_Transport")}

# id, источник, цель, подпись, способ трассировки
FLOWS = [
    ("F1", "Start", "T_CreateOrder", "", "h"),
    ("F2", "T_CreateOrder", "T_CheckOrder", "", "h"),
    ("F3", "T_CheckOrder", "G_OrderOk", "", "h"),
    ("F4", "G_OrderOk", "T_Clarify", "Нет", "up"),
    ("F5", "T_Clarify", "T_CheckOrder", "", "back_left"),
    ("F6", "G_OrderOk", "T_Quote", "Да", "h"),
    ("F7", "T_Quote", "T_Contract", "", "h"),
    ("F8", "T_Contract", "T_Pay", "", "h"),
    ("F9", "T_Pay", "G_Paid", "", "h"),
    ("F10", "G_Paid", "End_Cancel", "Нет", "down"),
    ("F11", "G_Paid", "T_Pick", "Да", "h"),
    ("F12", "T_Pick", "G_Full", "", "h"),
    ("F13", "G_Full", "T_Refill", "Нет", "down"),
    ("F14", "T_Refill", "T_Pick", "", "left_up"),
    ("F15", "G_Full", "T_Waybill", "Да", "h"),
    ("F16", "T_Waybill", "T_Route", "", "h"),
    ("F17", "T_Route", "T_Load", "", "h"),
    ("F18", "T_Load", "T_Transport", "", "h"),
    ("F19", "B_Delay", "T_Replan", "", "boundary"),
    ("F20", "T_Replan", "End_Notified", "", "h"),
    ("F21", "T_Transport", "T_Deliver", "", "h"),
    ("F22", "T_Deliver", "T_Accept", "", "h"),
    ("F23", "T_Accept", "G_Remarks", "", "h"),
    ("F24", "G_Remarks", "T_SignAct", "Нет", "h"),
    ("F25", "G_Remarks", "T_Claim", "Да", "down"),
    ("F26", "T_SignAct", "G_Merge", "", "h"),
    ("F27", "T_Claim", "G_Merge", "", "h"),
    ("F28", "G_Merge", "T_Close", "", "h"),
    ("F29", "T_Close", "End_Done", "", "h"),
]

# id, название, задача-источник
DATA = [
    ("D_Request", "Заявка на перевозку", "T_CreateOrder"),
    ("D_Invoice", "Договор-счёт", "T_Contract"),
    ("D_Waybill", "ТТН", "T_Waybill"),
    ("D_RouteSheet", "Маршрутный лист", "T_Route"),
    ("D_Act", "Акт приёмки", "T_SignAct"),
    ("D_Claim", "Претензия", "T_Accept"),
]

SIZE = {"startEvent": (36, 36), "endEvent": (36, 36), "exclusiveGateway": (50, 50),
        "userTask": (130, 80), "serviceTask": (130, 80)}


def layout():
    lanes, y = {}, POOL_Y
    for lid, name, rows in LANES:
        lanes[lid] = (y, int(rows * ROW_H), name)
        y += int(rows * ROW_H)
    pool_h = y - POOL_Y
    n_cols = max(n[3] for n in NODES.values()) + 1
    pool_w = FIRST_COL_X + n_cols * COL_W + 40
    shapes = {}
    for nid, (kind, _, lane, col, row) in NODES.items():
        w, h = SIZE[kind]
        cx = POOL_X + FIRST_COL_X + col * COL_W + COL_W / 2
        cy = lanes[lane][0] + row * ROW_H + ROW_H / 2 + (6 if lane != "Lane_Driver" else 26)
        shapes[nid] = (cx - w / 2, cy - h / 2, w, h)
    tx, ty, tw, th = shapes["T_Transport"]
    shapes["B_Delay"] = (tx + tw - 50, ty - 18, 36, 36)
    return lanes, pool_w, pool_h, shapes


def c(s):  # центр
    x, y, w, h = s
    return x + w / 2, y + h / 2


def route(kind, s, t):
    sx, sy = c(s); tx, ty = c(t)
    if kind == "h":
        x1, x2 = s[0] + s[2], t[0]
        if abs(sy - ty) < 1:
            return [(x1, sy), (x2, ty)]
        mx = (x1 + x2) / 2
        return [(x1, sy), (mx, sy), (mx, ty), (x2, ty)]
    if kind in ("up", "down"):
        y1 = s[1] if kind == "up" else s[1] + s[3]
        if abs(sx - tx) < 1:
            return [(sx, y1), (tx, t[1] + t[3] if kind == "up" else t[1])]
        return [(sx, y1), (sx, ty), (t[0], ty)]
    if kind == "back_left":  # из верхней дорожки назад к задаче ниже и левее
        return [(s[0], sy), (tx, sy), (tx, t[1])]
    if kind == "left_up":
        return [(s[0], sy), (tx, sy), (tx, t[1] + t[3])]
    if kind == "boundary":  # граничное событие на верхней кромке задачи -> вверх к цели
        return [(sx, s[1]), (sx, t[1] + t[3])]
    raise ValueError(kind)


def main() -> None:
    lanes, pool_w, pool_h, shapes = layout()
    incoming = {n: [] for n in list(NODES) + list(BOUNDARY)}
    outgoing = {n: [] for n in list(NODES) + list(BOUNDARY)}
    for fid, s, t, _, _ in FLOWS:
        outgoing[s].append(fid); incoming[t].append(fid)

    proc = []
    proc.append('    <bpmn:laneSet id="LaneSet_1">')
    for lid, name, _ in LANES:
        proc.append(f'      <bpmn:lane id="{lid}" name="{escape(name)}">')
        for nid, n in NODES.items():
            if n[2] == lid:
                proc.append(f"        <bpmn:flowNodeRef>{nid}</bpmn:flowNodeRef>")
        if lid == "Lane_Driver":
            proc.append("        <bpmn:flowNodeRef>B_Delay</bpmn:flowNodeRef>")
        proc.append("      </bpmn:lane>")
    proc.append("    </bpmn:laneSet>")

    data_for = {}
    for did, name, task in DATA:
        data_for.setdefault(task, []).append(did)

    for nid, (kind, name, *_rest) in NODES.items():
        attrs = f' id="{nid}"' + (f' name="{escape(name)}"' if name else "")
        body = [f"      <bpmn:incoming>{f}</bpmn:incoming>" for f in incoming[nid]]
        body += [f"      <bpmn:outgoing>{f}</bpmn:outgoing>" for f in outgoing[nid]]
        for did in data_for.get(nid, []):
            body.append(f'      <bpmn:dataOutputAssociation id="DA_{did}"><bpmn:targetRef>{did}Ref</bpmn:targetRef></bpmn:dataOutputAssociation>')
        proc.append(f"    <bpmn:{kind}{attrs}>")
        proc.extend(body)
        proc.append(f"    </bpmn:{kind}>")

    for bid, (name, host) in BOUNDARY.items():
        proc.append(f'    <bpmn:boundaryEvent id="{bid}" name="{escape(name)}" cancelActivity="false" attachedToRef="{host}">')
        proc.extend(f"      <bpmn:outgoing>{f}</bpmn:outgoing>" for f in outgoing[bid])
        proc.append('      <bpmn:timerEventDefinition id="TimerDef_Delay"><bpmn:timeDuration xsi:type="bpmn:tFormalExpression">PT2H</bpmn:timeDuration></bpmn:timerEventDefinition>')
        proc.append("    </bpmn:boundaryEvent>")

    for fid, s, t, name, _ in FLOWS:
        n = f' name="{name}"' if name else ""
        proc.append(f'    <bpmn:sequenceFlow id="{fid}"{n} sourceRef="{s}" targetRef="{t}" />')

    for did, name, _ in DATA:
        proc.append(f'    <bpmn:dataObjectReference id="{did}Ref" name="{escape(name)}" dataObjectRef="{did}" />')
        proc.append(f'    <bpmn:dataObject id="{did}" />')

    di = []
    di.append(f'      <bpmndi:BPMNShape id="Pool_di" bpmnElement="Participant_Logistics" isHorizontal="true">')
    di.append(f'        <dc:Bounds x="{POOL_X}" y="{POOL_Y}" width="{pool_w}" height="{pool_h}" />')
    di.append("      </bpmndi:BPMNShape>")
    for lid, (y, h, _) in lanes.items():
        di.append(f'      <bpmndi:BPMNShape id="{lid}_di" bpmnElement="{lid}" isHorizontal="true">')
        di.append(f'        <dc:Bounds x="{POOL_X + POOL_LABEL_W}" y="{y}" width="{pool_w - POOL_LABEL_W}" height="{h}" />')
        di.append("      </bpmndi:BPMNShape>")
    for nid, (x, y, w, h) in shapes.items():
        kind = NODES[nid][0] if nid in NODES else "boundaryEvent"
        marker = ' isMarkerVisible="true"' if kind == "exclusiveGateway" else ""
        di.append(f'      <bpmndi:BPMNShape id="{nid}_di" bpmnElement="{nid}"{marker}>')
        di.append(f'        <dc:Bounds x="{x:.0f}" y="{y:.0f}" width="{w}" height="{h}" />')
        if kind in ("startEvent", "endEvent", "exclusiveGateway", "boundaryEvent") and (nid in BOUNDARY or NODES[nid][1]):
            lw = 120
            ly = y + h + 5
            lx = x + w / 2 - lw / 2
            if kind == "exclusiveGateway":
                lx, ly = x - lw + 18, y + h - 4
            if kind == "endEvent" and nid != "End_Done":
                lx, ly = x + w + 6, y + 2
            if nid == "B_Delay":
                lx, ly = x + w + 4, y + 6
            di.append(f'        <bpmndi:BPMNLabel><dc:Bounds x="{lx:.0f}" y="{ly:.0f}" width="{lw}" height="36" /></bpmndi:BPMNLabel>')
        di.append("      </bpmndi:BPMNShape>")
    for fid, s, t, name, kind in FLOWS:
        pts = route(kind, shapes[s], shapes[t])
        di.append(f'      <bpmndi:BPMNEdge id="{fid}_di" bpmnElement="{fid}">')
        di.extend(f'        <di:waypoint x="{px:.0f}" y="{py:.0f}" />' for px, py in pts)
        if name:
            (ax, ay), (bx, by) = pts[0], pts[1]
            di.append(f'        <bpmndi:BPMNLabel><dc:Bounds x="{(ax + bx) / 2 + 6:.0f}" y="{(ay + by) / 2 - 20:.0f}" width="26" height="14" /></bpmndi:BPMNLabel>')
        di.append("      </bpmndi:BPMNEdge>")
    for did, name, task in DATA:
        tx, ty, tw, th = shapes[task]
        dx, dy = tx + tw + 4, ty - 62
        if NODES[task][2] == "Lane_Client":
            dx, dy = tx + 12, ty + th + 12
        shapes[did] = (dx, dy, 36, 50)
        di.append(f'      <bpmndi:BPMNShape id="{did}_di" bpmnElement="{did}Ref">')
        di.append(f'        <dc:Bounds x="{dx:.0f}" y="{dy:.0f}" width="36" height="50" />')
        di.append(f'        <bpmndi:BPMNLabel><dc:Bounds x="{dx + 40:.0f}" y="{dy + 16:.0f}" width="90" height="28" /></bpmndi:BPMNLabel>')
        di.append("      </bpmndi:BPMNShape>")
        sy = ty if dy < ty else ty + th
        ey = dy + 50 if dy < ty else dy
        di.append(f'      <bpmndi:BPMNEdge id="DA_{did}_di" bpmnElement="DA_{did}">')
        di.append(f'        <di:waypoint x="{tx + tw - 20:.0f}" y="{sy:.0f}" />')
        di.append(f'        <di:waypoint x="{dx + 10:.0f}" y="{ey:.0f}" />')
        di.append("      </bpmndi:BPMNEdge>")

    xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                  xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                  xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                  xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
                  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                  id="Definitions_LogiHub" targetNamespace="https://starpxand.github.io/logihub-wiki/bpmn"
                  exporter="LogiHub build_bpmn.py" exporterVersion="1.0">
  <bpmn:collaboration id="Collaboration_1">
    <bpmn:participant id="Participant_Logistics" name="ЛогиХаб: процесс управления логистикой" processRef="Process_Logistics" />
  </bpmn:collaboration>
  <bpmn:process id="Process_Logistics" name="Процесс управления логистикой" isExecutable="false">
{chr(10).join(proc)}
  </bpmn:process>
  <bpmndi:BPMNDiagram id="BPMNDiagram_1">
    <bpmndi:BPMNPlane id="BPMNPlane_1" bpmnElement="Collaboration_1">
{chr(10).join(di)}
    </bpmndi:BPMNPlane>
  </bpmndi:BPMNDiagram>
</bpmn:definitions>
'''
    OUT.write_text(xml, encoding="utf-8")
    print(f"OK: {OUT} ({len(NODES)} элементов, {len(FLOWS)} потоков)")


if __name__ == "__main__":
    main()
