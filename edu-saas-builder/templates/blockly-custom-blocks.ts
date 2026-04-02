/**
 * 한국어 Blockly 커스텀 블록 세트 — 교육용 코딩 SaaS
 *
 * 카테고리:
 *   1. 입출력 (5블록)
 *   2. 변수와 자료형 (5블록)
 *   3. 연산 (4블록)
 *   4. 조건문 (4블록)
 *   5. 반복문 (4블록)
 *   6. 리스트 (4블록)
 *   7. 함수 (3블록)
 *   8. 터틀 그래픽스 (6블록)
 *   9. 게임/인터랙션 (3블록)
 *
 * 총 38개 블록 + Python 제너레이터
 *
 * 사용법:
 *   import { registerAllBlocks, TOOLBOX_XML } from './blockly-custom-blocks';
 *   registerAllBlocks();
 *   // Blockly.inject('blocklyDiv', { toolbox: TOOLBOX_XML });
 */

import Blockly from 'blockly';
import { pythonGenerator, Order } from 'blockly/python';

// ============================================
// 1. 입출력 블록 (5개)
// ============================================

// 출력하기 (print)
Blockly.Blocks['ko_print'] = {
  init: function () {
    this.appendValueInput('TEXT').setCheck(null).appendField('출력하기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip('화면에 값을 출력합니다');
  },
};
pythonGenerator.forBlock['ko_print'] = function (block) {
  const text = pythonGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
  return `print(${text})\n`;
};

// 입력받기 (input)
Blockly.Blocks['ko_input'] = {
  init: function () {
    this.appendDummyInput().appendField('입력받기').appendField(new Blockly.FieldTextInput('무엇을 입력할까요?'), 'PROMPT');
    this.setOutput(true, 'String');
    this.setColour(160);
    this.setTooltip('사용자로부터 값을 입력받습니다');
  },
};
pythonGenerator.forBlock['ko_input'] = function (block) {
  const prompt = block.getFieldValue('PROMPT');
  return [`input("${prompt}")`, Order.FUNCTION_CALL];
};

// 숫자로 입력받기
Blockly.Blocks['ko_input_number'] = {
  init: function () {
    this.appendDummyInput().appendField('숫자 입력받기').appendField(new Blockly.FieldTextInput('숫자를 입력하세요'), 'PROMPT');
    this.setOutput(true, 'Number');
    this.setColour(160);
    this.setTooltip('사용자로부터 숫자를 입력받습니다');
  },
};
pythonGenerator.forBlock['ko_input_number'] = function (block) {
  const prompt = block.getFieldValue('PROMPT');
  return [`int(input("${prompt}"))`, Order.FUNCTION_CALL];
};

// 줄바꿈 없이 출력
Blockly.Blocks['ko_print_inline'] = {
  init: function () {
    this.appendValueInput('TEXT').setCheck(null).appendField('이어서 출력하기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
    this.setTooltip('줄바꿈 없이 출력합니다');
  },
};
pythonGenerator.forBlock['ko_print_inline'] = function (block) {
  const text = pythonGenerator.valueToCode(block, 'TEXT', Order.NONE) || "''";
  return `print(${text}, end="")\n`;
};

// 빈 줄 출력
Blockly.Blocks['ko_print_blank'] = {
  init: function () {
    this.appendDummyInput().appendField('빈 줄 출력하기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(160);
  },
};
pythonGenerator.forBlock['ko_print_blank'] = function () {
  return 'print()\n';
};

// ============================================
// 2. 변수와 자료형 (5개)
// ============================================

// 변수에 저장하기
Blockly.Blocks['ko_var_set'] = {
  init: function () {
    this.appendValueInput('VALUE')
      .setCheck(null)
      .appendField('변수')
      .appendField(new Blockly.FieldTextInput('이름'), 'VAR')
      .appendField('에 저장하기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(330);
    this.setTooltip('변수에 값을 저장합니다');
  },
};
pythonGenerator.forBlock['ko_var_set'] = function (block) {
  const varName = block.getFieldValue('VAR');
  const value = pythonGenerator.valueToCode(block, 'VALUE', Order.NONE) || '0';
  return `${varName} = ${value}\n`;
};

// 변수 값 가져오기
Blockly.Blocks['ko_var_get'] = {
  init: function () {
    this.appendDummyInput().appendField('변수').appendField(new Blockly.FieldTextInput('이름'), 'VAR').appendField('의 값');
    this.setOutput(true, null);
    this.setColour(330);
  },
};
pythonGenerator.forBlock['ko_var_get'] = function (block) {
  const varName = block.getFieldValue('VAR');
  return [varName, Order.ATOMIC];
};

// 문자열
Blockly.Blocks['ko_text'] = {
  init: function () {
    this.appendDummyInput().appendField('글자').appendField(new Blockly.FieldTextInput('안녕하세요'), 'TEXT');
    this.setOutput(true, 'String');
    this.setColour(160);
  },
};
pythonGenerator.forBlock['ko_text'] = function (block) {
  const text = block.getFieldValue('TEXT');
  return [`"${text}"`, Order.ATOMIC];
};

// 숫자
Blockly.Blocks['ko_number'] = {
  init: function () {
    this.appendDummyInput().appendField('숫자').appendField(new Blockly.FieldNumber(0), 'NUM');
    this.setOutput(true, 'Number');
    this.setColour(230);
  },
};
pythonGenerator.forBlock['ko_number'] = function (block) {
  const num = block.getFieldValue('NUM');
  return [String(num), Order.ATOMIC];
};

// 자료형 변환
Blockly.Blocks['ko_type_cast'] = {
  init: function () {
    this.appendValueInput('VALUE')
      .setCheck(null)
      .appendField(
        new Blockly.FieldDropdown([
          ['숫자로 바꾸기', 'int'],
          ['소수로 바꾸기', 'float'],
          ['글자로 바꾸기', 'str'],
        ]),
        'TYPE',
      );
    this.setOutput(true, null);
    this.setColour(230);
  },
};
pythonGenerator.forBlock['ko_type_cast'] = function (block) {
  const type = block.getFieldValue('TYPE');
  const value = pythonGenerator.valueToCode(block, 'VALUE', Order.NONE) || '0';
  return [`${type}(${value})`, Order.FUNCTION_CALL];
};

// ============================================
// 3. 연산 블록 (4개)
// ============================================

// 사칙연산
Blockly.Blocks['ko_math_op'] = {
  init: function () {
    this.appendValueInput('A').setCheck('Number');
    this.appendValueInput('B')
      .setCheck('Number')
      .appendField(
        new Blockly.FieldDropdown([
          ['더하기 +', '+'],
          ['빼기 -', '-'],
          ['곱하기 ×', '*'],
          ['나누기 ÷', '/'],
          ['나머지 %', '%'],
          ['몫 //', '//'],
          ['거듭제곱 **', '**'],
        ]),
        'OP',
      );
    this.setOutput(true, 'Number');
    this.setColour(230);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_math_op'] = function (block) {
  const a = pythonGenerator.valueToCode(block, 'A', Order.NONE) || '0';
  const b = pythonGenerator.valueToCode(block, 'B', Order.NONE) || '0';
  const op = block.getFieldValue('OP');
  return [`(${a} ${op} ${b})`, Order.NONE];
};

// 비교 연산
Blockly.Blocks['ko_compare'] = {
  init: function () {
    this.appendValueInput('A').setCheck(null);
    this.appendValueInput('B')
      .setCheck(null)
      .appendField(
        new Blockly.FieldDropdown([
          ['같다 ==', '=='],
          ['같지 않다 !=', '!='],
          ['크다 >', '>'],
          ['작다 <', '<'],
          ['크거나 같다 >=', '>='],
          ['작거나 같다 <=', '<='],
        ]),
        'OP',
      );
    this.setOutput(true, 'Boolean');
    this.setColour(210);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_compare'] = function (block) {
  const a = pythonGenerator.valueToCode(block, 'A', Order.NONE) || '0';
  const b = pythonGenerator.valueToCode(block, 'B', Order.NONE) || '0';
  const op = block.getFieldValue('OP');
  return [`${a} ${op} ${b}`, Order.RELATIONAL];
};

// 논리 연산
Blockly.Blocks['ko_logic'] = {
  init: function () {
    this.appendValueInput('A').setCheck('Boolean');
    this.appendValueInput('B')
      .setCheck('Boolean')
      .appendField(
        new Blockly.FieldDropdown([
          ['그리고', 'and'],
          ['또는', 'or'],
        ]),
        'OP',
      );
    this.setOutput(true, 'Boolean');
    this.setColour(210);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_logic'] = function (block) {
  const a = pythonGenerator.valueToCode(block, 'A', Order.NONE) || 'False';
  const b = pythonGenerator.valueToCode(block, 'B', Order.NONE) || 'False';
  const op = block.getFieldValue('OP');
  return [`${a} ${op} ${b}`, Order.LOGICAL_AND];
};

// 랜덤 숫자
Blockly.Blocks['ko_random'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('랜덤 숫자')
      .appendField(new Blockly.FieldNumber(1), 'MIN')
      .appendField('부터')
      .appendField(new Blockly.FieldNumber(10), 'MAX')
      .appendField('까지');
    this.setOutput(true, 'Number');
    this.setColour(230);
  },
};
pythonGenerator.forBlock['ko_random'] = function (block) {
  const min = block.getFieldValue('MIN');
  const max = block.getFieldValue('MAX');
  return [`random.randint(${min}, ${max})`, Order.FUNCTION_CALL];
};

// ============================================
// 4. 조건문 (4개)
// ============================================

// 만약 ~이면
Blockly.Blocks['ko_if'] = {
  init: function () {
    this.appendValueInput('CONDITION').setCheck('Boolean').appendField('만약');
    this.appendDummyInput().appendField('이면');
    this.appendStatementInput('DO').setCheck(null);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
  },
};
pythonGenerator.forBlock['ko_if'] = function (block) {
  const condition = pythonGenerator.valueToCode(block, 'CONDITION', Order.NONE) || 'False';
  const doCode = pythonGenerator.statementToCode(block, 'DO') || '    pass\n';
  return `if ${condition}:\n${doCode}`;
};

// 만약 ~이면 / 아니면
Blockly.Blocks['ko_if_else'] = {
  init: function () {
    this.appendValueInput('CONDITION').setCheck('Boolean').appendField('만약');
    this.appendDummyInput().appendField('이면');
    this.appendStatementInput('DO').setCheck(null);
    this.appendDummyInput().appendField('아니면');
    this.appendStatementInput('ELSE').setCheck(null);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
  },
};
pythonGenerator.forBlock['ko_if_else'] = function (block) {
  const condition = pythonGenerator.valueToCode(block, 'CONDITION', Order.NONE) || 'False';
  const doCode = pythonGenerator.statementToCode(block, 'DO') || '    pass\n';
  const elseCode = pythonGenerator.statementToCode(block, 'ELSE') || '    pass\n';
  return `if ${condition}:\n${doCode}else:\n${elseCode}`;
};

// 만약 / 아니면 만약 / 아니면
Blockly.Blocks['ko_if_elif_else'] = {
  init: function () {
    this.appendValueInput('COND1').setCheck('Boolean').appendField('만약');
    this.appendStatementInput('DO1');
    this.appendValueInput('COND2').setCheck('Boolean').appendField('아니면 만약');
    this.appendStatementInput('DO2');
    this.appendDummyInput().appendField('아니면');
    this.appendStatementInput('ELSE');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(210);
  },
};
pythonGenerator.forBlock['ko_if_elif_else'] = function (block) {
  const c1 = pythonGenerator.valueToCode(block, 'COND1', Order.NONE) || 'False';
  const d1 = pythonGenerator.statementToCode(block, 'DO1') || '    pass\n';
  const c2 = pythonGenerator.valueToCode(block, 'COND2', Order.NONE) || 'False';
  const d2 = pythonGenerator.statementToCode(block, 'DO2') || '    pass\n';
  const el = pythonGenerator.statementToCode(block, 'ELSE') || '    pass\n';
  return `if ${c1}:\n${d1}elif ${c2}:\n${d2}else:\n${el}`;
};

// 참/거짓
Blockly.Blocks['ko_boolean'] = {
  init: function () {
    this.appendDummyInput().appendField(
      new Blockly.FieldDropdown([
        ['참', 'True'],
        ['거짓', 'False'],
      ]),
      'VALUE',
    );
    this.setOutput(true, 'Boolean');
    this.setColour(210);
  },
};
pythonGenerator.forBlock['ko_boolean'] = function (block) {
  return [block.getFieldValue('VALUE'), Order.ATOMIC];
};

// ============================================
// 5. 반복문 (4개)
// ============================================

// N번 반복하기
Blockly.Blocks['ko_repeat'] = {
  init: function () {
    this.appendValueInput('TIMES').setCheck('Number');
    this.appendDummyInput().appendField('번 반복하기');
    this.appendStatementInput('DO').setCheck(null);
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
  },
};
pythonGenerator.forBlock['ko_repeat'] = function (block) {
  const times = pythonGenerator.valueToCode(block, 'TIMES', Order.NONE) || '0';
  const doCode = pythonGenerator.statementToCode(block, 'DO') || '    pass\n';
  return `for _i in range(${times}):\n${doCode}`;
};

// ~부터 ~까지 반복 (변수 사용)
Blockly.Blocks['ko_for_range'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('변수')
      .appendField(new Blockly.FieldTextInput('i'), 'VAR')
      .appendField('를');
    this.appendValueInput('FROM').setCheck('Number');
    this.appendDummyInput().appendField('부터');
    this.appendValueInput('TO').setCheck('Number');
    this.appendDummyInput().appendField('까지 반복');
    this.appendStatementInput('DO');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_for_range'] = function (block) {
  const varName = block.getFieldValue('VAR');
  const from = pythonGenerator.valueToCode(block, 'FROM', Order.NONE) || '0';
  const to = pythonGenerator.valueToCode(block, 'TO', Order.NONE) || '10';
  const doCode = pythonGenerator.statementToCode(block, 'DO') || '    pass\n';
  return `for ${varName} in range(${from}, ${to} + 1):\n${doCode}`;
};

// ~하는 동안 반복 (while)
Blockly.Blocks['ko_while'] = {
  init: function () {
    this.appendValueInput('CONDITION').setCheck('Boolean');
    this.appendDummyInput().appendField('하는 동안 반복하기');
    this.appendStatementInput('DO');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(120);
  },
};
pythonGenerator.forBlock['ko_while'] = function (block) {
  const cond = pythonGenerator.valueToCode(block, 'CONDITION', Order.NONE) || 'False';
  const doCode = pythonGenerator.statementToCode(block, 'DO') || '    pass\n';
  return `while ${cond}:\n${doCode}`;
};

// 반복 멈추기 (break)
Blockly.Blocks['ko_break'] = {
  init: function () {
    this.appendDummyInput().appendField('반복 멈추기');
    this.setPreviousStatement(true, null);
    this.setColour(120);
  },
};
pythonGenerator.forBlock['ko_break'] = function () {
  return 'break\n';
};

// ============================================
// 6. 리스트 (4개)
// ============================================

// 빈 리스트 만들기
Blockly.Blocks['ko_list_create'] = {
  init: function () {
    this.appendDummyInput().appendField('빈 리스트 만들기');
    this.setOutput(true, 'Array');
    this.setColour(260);
  },
};
pythonGenerator.forBlock['ko_list_create'] = function () {
  return ['[]', Order.ATOMIC];
};

// 리스트에 추가
Blockly.Blocks['ko_list_append'] = {
  init: function () {
    this.appendValueInput('LIST').appendField('리스트');
    this.appendValueInput('ITEM').appendField('에 추가하기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(260);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_list_append'] = function (block) {
  const list = pythonGenerator.valueToCode(block, 'LIST', Order.NONE) || '[]';
  const item = pythonGenerator.valueToCode(block, 'ITEM', Order.NONE) || '0';
  return `${list}.append(${item})\n`;
};

// 리스트 N번째 가져오기
Blockly.Blocks['ko_list_get'] = {
  init: function () {
    this.appendValueInput('LIST').appendField('리스트');
    this.appendValueInput('INDEX').setCheck('Number').appendField('의');
    this.appendDummyInput().appendField('번째 값');
    this.setOutput(true, null);
    this.setColour(260);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_list_get'] = function (block) {
  const list = pythonGenerator.valueToCode(block, 'LIST', Order.NONE) || '[]';
  const index = pythonGenerator.valueToCode(block, 'INDEX', Order.NONE) || '0';
  return [`${list}[${index}]`, Order.MEMBER];
};

// 리스트 길이
Blockly.Blocks['ko_list_length'] = {
  init: function () {
    this.appendValueInput('LIST').appendField('리스트');
    this.appendDummyInput().appendField('의 길이');
    this.setOutput(true, 'Number');
    this.setColour(260);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_list_length'] = function (block) {
  const list = pythonGenerator.valueToCode(block, 'LIST', Order.NONE) || '[]';
  return [`len(${list})`, Order.FUNCTION_CALL];
};

// ============================================
// 7. 함수 (3개)
// ============================================

// 함수 만들기
Blockly.Blocks['ko_function_def'] = {
  init: function () {
    this.appendDummyInput().appendField('함수 만들기').appendField(new Blockly.FieldTextInput('인사하기'), 'NAME');
    this.appendStatementInput('BODY');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
  },
};
pythonGenerator.forBlock['ko_function_def'] = function (block) {
  const name = block.getFieldValue('NAME');
  const body = pythonGenerator.statementToCode(block, 'BODY') || '    pass\n';
  return `def ${name}():\n${body}\n`;
};

// 매개변수 있는 함수
Blockly.Blocks['ko_function_def_param'] = {
  init: function () {
    this.appendDummyInput()
      .appendField('함수 만들기')
      .appendField(new Blockly.FieldTextInput('더하기'), 'NAME')
      .appendField('(')
      .appendField(new Blockly.FieldTextInput('a, b'), 'PARAMS')
      .appendField(')');
    this.appendStatementInput('BODY');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
  },
};
pythonGenerator.forBlock['ko_function_def_param'] = function (block) {
  const name = block.getFieldValue('NAME');
  const params = block.getFieldValue('PARAMS');
  const body = pythonGenerator.statementToCode(block, 'BODY') || '    pass\n';
  return `def ${name}(${params}):\n${body}\n`;
};

// 함수 호출
Blockly.Blocks['ko_function_call'] = {
  init: function () {
    this.appendDummyInput().appendField('함수 실행하기').appendField(new Blockly.FieldTextInput('인사하기'), 'NAME').appendField('()');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(290);
  },
};
pythonGenerator.forBlock['ko_function_call'] = function (block) {
  const name = block.getFieldValue('NAME');
  return `${name}()\n`;
};

// ============================================
// 8. 터틀 그래픽스 (6개)
// ============================================

// 앞으로 이동
Blockly.Blocks['ko_turtle_forward'] = {
  init: function () {
    this.appendValueInput('DISTANCE').setCheck('Number').appendField('🐢 앞으로');
    this.appendDummyInput().appendField('만큼 이동');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_turtle_forward'] = function (block) {
  const dist = pythonGenerator.valueToCode(block, 'DISTANCE', Order.NONE) || '100';
  return `t.forward(${dist})\n`;
};

// 회전
Blockly.Blocks['ko_turtle_turn'] = {
  init: function () {
    this.appendDummyInput().appendField('🐢').appendField(
      new Blockly.FieldDropdown([
        ['오른쪽으로', 'right'],
        ['왼쪽으로', 'left'],
      ]),
      'DIR',
    );
    this.appendValueInput('ANGLE').setCheck('Number');
    this.appendDummyInput().appendField('도 회전');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_turtle_turn'] = function (block) {
  const dir = block.getFieldValue('DIR');
  const angle = pythonGenerator.valueToCode(block, 'ANGLE', Order.NONE) || '90';
  return `t.${dir}(${angle})\n`;
};

// 펜 올리기/내리기
Blockly.Blocks['ko_turtle_pen'] = {
  init: function () {
    this.appendDummyInput().appendField('🐢 펜').appendField(
      new Blockly.FieldDropdown([
        ['내리기 ✏️', 'pendown'],
        ['올리기', 'penup'],
      ]),
      'ACTION',
    );
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
  },
};
pythonGenerator.forBlock['ko_turtle_pen'] = function (block) {
  return `t.${block.getFieldValue('ACTION')}()\n`;
};

// 색상 변경
Blockly.Blocks['ko_turtle_color'] = {
  init: function () {
    this.appendDummyInput().appendField('🐢 색상 바꾸기').appendField(new Blockly.FieldColour('#ff0000'), 'COLOR');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
  },
};
pythonGenerator.forBlock['ko_turtle_color'] = function (block) {
  const color = block.getFieldValue('COLOR');
  return `t.color("${color}")\n`;
};

// 원 그리기
Blockly.Blocks['ko_turtle_circle'] = {
  init: function () {
    this.appendValueInput('RADIUS').setCheck('Number').appendField('🐢 원 그리기 반지름');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_turtle_circle'] = function (block) {
  const r = pythonGenerator.valueToCode(block, 'RADIUS', Order.NONE) || '50';
  return `t.circle(${r})\n`;
};

// 위치로 이동
Blockly.Blocks['ko_turtle_goto'] = {
  init: function () {
    this.appendDummyInput().appendField('🐢 이동하기 x:').appendField(new Blockly.FieldNumber(0), 'X').appendField('y:').appendField(new Blockly.FieldNumber(0), 'Y');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(65);
  },
};
pythonGenerator.forBlock['ko_turtle_goto'] = function (block) {
  return `t.goto(${block.getFieldValue('X')}, ${block.getFieldValue('Y')})\n`;
};

// ============================================
// 9. 게임/인터랙션 (3개)
// ============================================

// 기다리기
Blockly.Blocks['ko_wait'] = {
  init: function () {
    this.appendValueInput('SECONDS').setCheck('Number').appendField('⏱️');
    this.appendDummyInput().appendField('초 기다리기');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(20);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_wait'] = function (block) {
  const seconds = pythonGenerator.valueToCode(block, 'SECONDS', Order.NONE) || '1';
  return `import time\ntime.sleep(${seconds})\n`;
};

// 주석 (메모)
Blockly.Blocks['ko_comment'] = {
  init: function () {
    this.appendDummyInput().appendField('📝 메모:').appendField(new Blockly.FieldTextInput('여기에 설명을 적어요'), 'TEXT');
    this.setPreviousStatement(true, null);
    this.setNextStatement(true, null);
    this.setColour(20);
  },
};
pythonGenerator.forBlock['ko_comment'] = function (block) {
  return `# ${block.getFieldValue('TEXT')}\n`;
};

// 글자 합치기
Blockly.Blocks['ko_text_join'] = {
  init: function () {
    this.appendValueInput('A');
    this.appendValueInput('B').appendField('와');
    this.appendDummyInput().appendField('합치기');
    this.setOutput(true, 'String');
    this.setColour(160);
    this.setInputsInline(true);
  },
};
pythonGenerator.forBlock['ko_text_join'] = function (block) {
  const a = pythonGenerator.valueToCode(block, 'A', Order.NONE) || "''";
  const b = pythonGenerator.valueToCode(block, 'B', Order.NONE) || "''";
  return [`str(${a}) + str(${b})`, Order.ADDITION];
};

// ============================================
// 등록 함수 & 툴박스 XML
// ============================================

export function registerAllBlocks(): void {
  // 모든 블록은 import 시점에 이미 Blockly.Blocks에 등록됨
  // 이 함수는 명시적 초기화 호출용
}

export const TOOLBOX_XML = `
<xml xmlns="https://developers.google.com/blockly/xml" id="toolbox" style="display: none">
  <category name="📢 입출력" colour="160">
    <block type="ko_print"></block>
    <block type="ko_print_inline"></block>
    <block type="ko_print_blank"></block>
    <block type="ko_input"></block>
    <block type="ko_input_number"></block>
  </category>
  <category name="📦 변수" colour="330">
    <block type="ko_var_set"></block>
    <block type="ko_var_get"></block>
    <block type="ko_text"></block>
    <block type="ko_number"></block>
    <block type="ko_type_cast"></block>
  </category>
  <category name="🔢 연산" colour="230">
    <block type="ko_math_op"></block>
    <block type="ko_compare"></block>
    <block type="ko_logic"></block>
    <block type="ko_random"></block>
  </category>
  <category name="❓ 조건" colour="210">
    <block type="ko_if"></block>
    <block type="ko_if_else"></block>
    <block type="ko_if_elif_else"></block>
    <block type="ko_boolean"></block>
  </category>
  <category name="🔄 반복" colour="120">
    <block type="ko_repeat"></block>
    <block type="ko_for_range"></block>
    <block type="ko_while"></block>
    <block type="ko_break"></block>
  </category>
  <category name="📋 리스트" colour="260">
    <block type="ko_list_create"></block>
    <block type="ko_list_append"></block>
    <block type="ko_list_get"></block>
    <block type="ko_list_length"></block>
  </category>
  <category name="🔧 함수" colour="290">
    <block type="ko_function_def"></block>
    <block type="ko_function_def_param"></block>
    <block type="ko_function_call"></block>
  </category>
  <category name="🐢 터틀" colour="65">
    <block type="ko_turtle_forward"></block>
    <block type="ko_turtle_turn"></block>
    <block type="ko_turtle_pen"></block>
    <block type="ko_turtle_color"></block>
    <block type="ko_turtle_circle"></block>
    <block type="ko_turtle_goto"></block>
  </category>
  <category name="⚙️ 기타" colour="20">
    <block type="ko_wait"></block>
    <block type="ko_comment"></block>
    <block type="ko_text_join"></block>
  </category>
</xml>
`;
