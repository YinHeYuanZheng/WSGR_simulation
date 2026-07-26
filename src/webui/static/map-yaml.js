(function (root) {
  'use strict';

  const SIMPLE_KEY = /^[A-Za-z_][A-Za-z0-9_-]*$/;

  function stripComment(line) {
    let quote = null;
    for (let index = 0; index < line.length; index += 1) {
      const char = line[index];
      if ((char === '"' || char === "'") && line[index - 1] !== '\\') {
        quote = quote === char ? null : (quote || char);
      }
      if (char === '#' && quote === null && (index === 0 || /\s/.test(line[index - 1]))) {
        return line.slice(0, index);
      }
    }
    return line;
  }

  function splitKeyValue(text) {
    let quote = null;
    for (let index = 0; index < text.length; index += 1) {
      const char = text[index];
      if ((char === '"' || char === "'") && text[index - 1] !== '\\') {
        quote = quote === char ? null : (quote || char);
      }
      if (char === ':' && quote === null) {
        return [text.slice(0, index).trim(), text.slice(index + 1).trim()];
      }
    }
    return null;
  }

  function parseScalar(raw) {
    const text = raw.trim();
    if (text === '') return '';
    if (text === 'null' || text === '~') return null;
    if (text === 'true') return true;
    if (text === 'false') return false;
    if (/^-?(?:0|[1-9]\d*)(?:\.\d+)?$/.test(text)) return Number(text);
    if (text.startsWith('"') && text.endsWith('"')) return JSON.parse(text);
    if (text.startsWith("'") && text.endsWith("'")) return text.slice(1, -1).replace(/''/g, "'");
    if (text === '[]') return [];
    if (text === '{}') return {};
    return text;
  }

  function parse(source) {
    const lines = String(source)
      .replace(/^\uFEFF/, '')
      .replace(/\r\n?/g, '\n')
      .split('\n')
      .map((raw, sourceIndex) => {
        if (raw.includes('\t')) throw new Error(`第 ${sourceIndex + 1} 行包含 Tab，请使用空格缩进`);
        const withoutComment = stripComment(raw).replace(/\s+$/, '');
        if (!withoutComment.trim() || withoutComment.trim() === '---' || withoutComment.trim() === '...') return null;
        const indent = withoutComment.length - withoutComment.trimStart().length;
        return { indent, text: withoutComment.trimStart(), sourceIndex };
      })
      .filter(Boolean);

    if (!lines.length) throw new Error('YAML 文件为空');
    let cursor = 0;

    function parseMap(indent) {
      const result = {};
      while (cursor < lines.length) {
        const line = lines[cursor];
        if (line.indent < indent) break;
        if (line.indent > indent) throw new Error(`第 ${line.sourceIndex + 1} 行缩进层级不正确`);
        if (line.text.startsWith('-')) break;
        const pair = splitKeyValue(line.text);
        if (!pair || !pair[0]) throw new Error(`第 ${line.sourceIndex + 1} 行不是有效的 key: value`);
        const [rawKey, rawValue] = pair;
        const key = parseScalar(rawKey);
        cursor += 1;
        if (rawValue !== '') {
          result[String(key)] = parseScalar(rawValue);
        } else if (cursor < lines.length && lines[cursor].indent > indent) {
          result[String(key)] = parseNode(lines[cursor].indent);
        } else {
          result[String(key)] = null;
        }
      }
      return result;
    }

    function parseSequence(indent) {
      const result = [];
      while (cursor < lines.length) {
        const line = lines[cursor];
        if (line.indent < indent) break;
        if (line.indent !== indent || !line.text.startsWith('-')) break;
        const rest = line.text.slice(1).trim();
        cursor += 1;
        if (rest === '') {
          result.push(cursor < lines.length && lines[cursor].indent > indent
            ? parseNode(lines[cursor].indent)
            : null);
          continue;
        }
        const pair = splitKeyValue(rest);
        if (!pair) {
          result.push(parseScalar(rest));
          continue;
        }
        const item = {};
        const [rawKey, rawValue] = pair;
        const key = String(parseScalar(rawKey));
        if (rawValue !== '') {
          item[key] = parseScalar(rawValue);
        } else if (cursor < lines.length && lines[cursor].indent > indent) {
          item[key] = parseNode(lines[cursor].indent);
        } else {
          item[key] = null;
        }
        if (cursor < lines.length && lines[cursor].indent > indent) {
          const continuationIndent = lines[cursor].indent;
          const continuation = parseMap(continuationIndent);
          Object.assign(item, continuation);
        }
        result.push(item);
      }
      return result;
    }

    function parseNode(indent) {
      if (cursor >= lines.length) return null;
      return lines[cursor].text.startsWith('-') ? parseSequence(indent) : parseMap(indent);
    }

    const output = parseNode(lines[0].indent);
    if (cursor !== lines.length) {
      const line = lines[cursor];
      throw new Error(`第 ${line.sourceIndex + 1} 行无法解析`);
    }
    return output;
  }

  function quoteString(value) {
    return JSON.stringify(String(value));
  }

  function scalar(value) {
    if (value === null || value === undefined) return 'null';
    if (typeof value === 'boolean') return value ? 'true' : 'false';
    if (typeof value === 'number') {
      if (!Number.isFinite(value)) throw new Error('YAML 不能保存无效数字');
      return String(value);
    }
    return quoteString(value);
  }

  function keyText(key) {
    return SIMPLE_KEY.test(key) ? key : quoteString(key);
  }

  function stringify(value) {
    const lines = [];

    function write(current, indent, sequencePrefix) {
      const pad = ' '.repeat(indent);
      if (Array.isArray(current)) {
        if (!current.length) {
          lines.push(`${pad}${sequencePrefix ? '- ' : ''}[]`);
          return;
        }
        current.forEach(item => {
          if (item && typeof item === 'object' && !Array.isArray(item)) {
            const entries = Object.entries(item);
            if (!entries.length) {
              lines.push(`${pad}- {}`);
              return;
            }
            const [firstKey, firstValue] = entries[0];
            if (firstValue && typeof firstValue === 'object') {
              lines.push(`${pad}- ${keyText(firstKey)}:`);
              write(firstValue, indent + 4, false);
            } else {
              lines.push(`${pad}- ${keyText(firstKey)}: ${scalar(firstValue)}`);
            }
            entries.slice(1).forEach(([key, itemValue]) => writePair(key, itemValue, indent + 2));
          } else if (Array.isArray(item)) {
            lines.push(`${pad}-`);
            write(item, indent + 2, false);
          } else {
            lines.push(`${pad}- ${scalar(item)}`);
          }
        });
        return;
      }
      Object.entries(current || {}).forEach(([key, itemValue]) => writePair(key, itemValue, indent));
    }

    function writePair(key, itemValue, indent) {
      const pad = ' '.repeat(indent);
      if (Array.isArray(itemValue)) {
        if (!itemValue.length) {
          lines.push(`${pad}${keyText(key)}: []`);
        } else {
          lines.push(`${pad}${keyText(key)}:`);
          write(itemValue, indent + 2, false);
        }
      } else if (itemValue && typeof itemValue === 'object') {
        const entries = Object.keys(itemValue);
        if (!entries.length) {
          lines.push(`${pad}${keyText(key)}: {}`);
        } else {
          lines.push(`${pad}${keyText(key)}:`);
          write(itemValue, indent + 2, false);
        }
      } else {
        lines.push(`${pad}${keyText(key)}: ${scalar(itemValue)}`);
      }
    }

    write(value, 0, false);
    return `${lines.join('\n')}\n`;
  }

  const api = { parse, stringify };
  root.MapYaml = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
}(typeof globalThis !== 'undefined' ? globalThis : this));
