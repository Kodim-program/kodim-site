function getDigitsMap(str) {
    const map = {
        '1': '', '2': '', '3': '', '4': '', '5': '', '6': '', '7': '', '8': '', '9': ''
    };
    for (const ch of str) {
        if (map.hasOwnProperty(ch)) map[ch] += ch;
    }
    return map;
}

function addDigitsToMap(map, str, allowed = null) {
    for (const ch of str) {
        if (map.hasOwnProperty(ch) && (!allowed || allowed.includes(ch))) {
            map[ch] += ch;
        }
    }
}

function calculateResults(result) {
    // Зчитування дати народження з трьох select: рік, місяць, день
    const year_ = document.querySelector('#birth-year')?.value;
    const month_ = document.querySelector('#birth-month')?.value;
    const day_ = document.querySelector('#birth-day')?.value;
    const dateBirthInput = (year_ && month_ && day_) ? `${year_}-${month_.padStart(2, '0')}-${day_.padStart(2, '0')}` : '';
    //console.log("Date of Birth Input:", dateBirthInput);
    if (!dateBirthInput) {
        alert("Необхідно ввести дату народження.");
        return;
    }

    const db = dateBirthInput.split('-');
    
    if (db.length !== 3) {
        alert("Invalid date format.");
        return;
    }

    const [year, month, day] = db.map(Number);
    const dbStr = `${year}${month}${day}`;
    //console.log("Date of Birth String:", dbStr);
    // #1
    const map = getDigitsMap(dbStr);
    //console.log(map)
    // #2
    let sum = dbStr.split('').reduce((acc, d) => acc + Number(d), 0);
    const sum2 = String(sum);
    addDigitsToMap(map, sum2, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    
    //console.log("Sum 2:", sum2);
    //console.log(map)
    // #3
    let sum3 = 0;
    if (sum2.length > 1 && sum2 !== '11') {
        sum3 = String(sum2.split('').reduce((acc, d) => acc + Number(d), 0));  
        if (Number(sum3) === 10){
            sum3 = '1'; // Якщо сума 10, то беремо 1
        }  
        if (sum3) {
            addDigitsToMap(map, sum3, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
            /*if (Number(sum3) != 11) {
                sum3 = sum2.split('').reduce((acc, d) => acc + Number(d), 0);
            }*/
           if (sum3.length > 1 && sum3 !== '11') {
                sum3 = String(sum3.split('').reduce((acc, d) => acc + Number(d), 0));
                if (Number(sum3) === 10){
                    sum3 = '1'; // Якщо сума 10, то беремо 1
                }   
                //addDigitsToMap(map, sum3, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
            } 
        }
    } else {
        sum3 = sum2;
    }
    //console.log("Sum 3:", sum3);
    //console.log(map)
    // Якщо сума дорівнює 11, то беремо 1 цифрe з дати народження не 0
    // #4
    let sum4 = sum2 - 2 * (String(day).length == 1 ? day : Number(String(day)[0]));
    if (sum4 > 0) {
        const sum4Str = String(sum4);
        addDigitsToMap(map, sum4Str, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    }
    //#5
    let sum5 = 0;
    if (sum4 > 0) sum5 = String(sum4).split('').reduce((acc, d) => acc + Number(d), 0);
    if (sum5 > 0) {
        sum5 = String(sum5);
        addDigitsToMap(map, sum5, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    }
      

    // Відображення результатів

    const btnElements = document.querySelectorAll('.btn');
    btnElements.forEach(btn => {
        const chr = btn.querySelector('.chr p');
        const zd = btn.querySelector('.zd p');
        const ud = btn.querySelector('.ud p');
        const pm = btn.querySelector('.pm p');
        const en = btn.querySelector('.en p');
        const pv = btn.querySelector('.pv p');
        const tm = btn.querySelector('.tm p');
        const cl = btn.querySelector('.cl p');
        const lg = btn.querySelector('.lg p');
        const ob = btn.querySelector('.ob p');
        const fam = btn.querySelector('.sm p');
        const interest = btn.querySelector('.ck p');
        const work = btn.querySelector('.pr p');
        const zvychky = btn.querySelector('.zv p');
        const pobut = btn.querySelector('.pb p');
        if (pv) pv.textContent = sum3;
        if (tm) tm.textContent = (map['7'].length + map['5'].length + map['3'].length) != 0 ? map['7'].length + map['5'].length + map['3'].length : '--';
        if (cl) cl.textContent = (map['1'].length + map['4'].length + map['7'].length) != 0 ? map['1'].length + map['4'].length + map['7'].length : '--';
        if (chr) chr.textContent = (map['1']) ? map['1'] : '--';
        if (zd) zd.textContent = (map['4']) ? map['4'] : '--';
        if (ud) ud.textContent = (map['7']) ? map['7'] : '--';
        if (pm) pm.textContent = (map['9']) ? map['9'] : '--';
        if (en) en.textContent = (map['2']) ? map['2'] : '--';
        if (interest) interest.textContent = (map['3']) ? map['3'] : '--';
        if (lg) lg.textContent = (map['5']) ? map['5'] : '--';
        if (work) work.textContent = (map['6']) ? map['6'] : '--';
        if (ob) ob.textContent = (map['8']) ? map['8'] : '--';

        if (pobut) pobut.textContent = (map['4'].length + map['5'].length + map['6'].length) != 0 ? map['4'].length + map['5'].length + map['6'].length : '--';
        if (zvychky) zvychky.textContent = (map['3'].length + map['6'].length + map['9'].length) != 0 ? map['3'].length + map['6'].length + map['9'].length : '--';
        if (fam) fam.textContent = (map['2'].length + map['5'].length + map['8'].length) != 0 ? map['2'].length + map['5'].length + map['8'].length : '--';
    });
    const text_psycho = document.querySelector('.text_psycho p');
    if (text_psycho) {
        text_psycho.textContent = `${(map['1']) ? map['1'] : '--'}/${(map['2']) ? map['2'] : '--'}/${(map['3']) ? map['3'] : '--'}/
        ${(map['4']) ? map['4'] : '--'}/${(map['5']) ? map['5'] : '--'}/${(map['6']) ? map['6'] : '--'}/${(map['7']) ? map['7'] : '--'}/
        ${(map['8']) ? map['8'] : '--'}/${(map['9']) ? map['9'] : '--'}/ПВ-${sum3}`;
    }
}

function copyPsychoResult() {
    const textPsycho = document.querySelector('.text_psycho p');
    if (textPsycho) {
    
        const text = textPsycho.textContent.replace(/\s*\n\s*/g, '').replace(/\s{2,}/g, ' ').trim();
        // Спроба через Clipboard API
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text)
                .then(() => alert('Результат скопійовано!'))
                .catch(() => fallbackCopyTextToClipboard(text));
        } else {
            fallbackCopyTextToClipboard(text);
        }
    }
}

// Фолбек для старих браузерів/платформ
function fallbackCopyTextToClipboard(text) {
    const textarea = document.createElement('textarea');
    textarea.value = text;
    // Уникнути прокрутки сторінки на мобільних
    textarea.style.position = 'fixed';
    textarea.style.top = 0;
    textarea.style.left = 0;
    textarea.style.width = '2em';
    textarea.style.height = '2em';
    textarea.style.padding = 0;
    textarea.style.border = 'none';
    textarea.style.outline = 'none';
    textarea.style.boxShadow = 'none';
    textarea.style.background = 'transparent';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    try {
        const successful = document.execCommand('copy');
        alert(successful ? 'Результат скопійовано!' : 'Не вдалося скопіювати результат.');
    } catch (err) {
        alert('Не вдалося скопіювати результат.');
    }

    document.body.removeChild(textarea);
}
// Додаємо кнопку для копіювання результату
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.createElement('button');
    btn.textContent = 'Копіювати результат';
    btn.className = 'copy-psycho-btn';
    btn.style.margin = '10px 0';

    btn.addEventListener('click', copyPsychoResult);

    const textPsychoBlock = document.querySelector('.text_psycho');
    if (textPsychoBlock) {
        textPsychoBlock.appendChild(btn);
    }
});

function saveResults() {
    const name = document.getElementById("name").value || "результат";

    const resultBlock = document.querySelector(".output_user");

    html2canvas(resultBlock).then(canvas => {
        const link = document.createElement("a");
        link.download = `${name}_результат.png`;
        link.href = canvas.toDataURL();
        link.click();
    });
}

