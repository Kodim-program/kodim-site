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
    const dateBirthInput = document.querySelector('input[id="birthday"]').value;
    if (!dateBirthInput) {
        console.error("Birthday input is empty.");
        return;
    }

    const db = dateBirthInput.split('-');
    const dateNum = db[2][0]=== '0' ? db[2][1] : db[2];
    if (db.length !== 3) {
        console.error("Invalid date format.");
        return;
    }

    const [year, month, day] = db.map(Number);
    const dbStr = `${year}${month}${day}`;
    console.log("Date of Birth String:", dbStr);
    // #1
    const map = getDigitsMap(dbStr);
    console.log(map)
    // #2
    let sum = dbStr.split('').reduce((acc, d) => acc + Number(d), 0);
    const sumStr = String(sum);
    addDigitsToMap(map, sumStr, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
    let sum2 = '';
    if (sum != 11) sum2 = sumStr;
    console.log("Sum 2:", sum2);
    console.log(map)
    // #3
    let sum3 = 0;
    sum3 = String(sum2.split('').reduce((acc, d) => acc + Number(d), 0));    
    if (sum3) {
        addDigitsToMap(map, sum3, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
        /*if (Number(sum3) != 11) {
            sum3 = sum2.split('').reduce((acc, d) => acc + Number(d), 0);
        }*/
    }
    console.log("Sum 3:", sum3);
    console.log(map)
    // Якщо сума дорівнює 11, то беремо 1 цифрe з дати народження не 0
    // #4
    let sum4 = sum2 - 2 * dateNum;
    if (sum4 > 0) {
        const sum4Str = String(sum4);
        addDigitsToMap(map, sum4Str, ['1', '2', '3', '4', '5', '6', '7', '8', '9']);
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
        if (tm) tm.textContent = map['7'].length + map['5'].length + map['3'].length;
        if (cl) cl.textContent = map['1'].length + map['4'].length + map['7'].length;
        if (chr) chr.textContent = map['1'];
        if (zd) zd.textContent = map['4'];
        if (ud) ud.textContent = map['7'];
        if (pm) pm.textContent = map['9'];
        if (en) en.textContent = map['2'];
        if (interest) interest.textContent = map['3'];
        if (lg) lg.textContent = map['5'];
        if (work) work.textContent = map['6'];
        if (ob) ob.textContent = map['8'];

        if (pobut) pobut.textContent = map['4'].length + map['5'].length + map['6'].length;
        if (zvychky) zvychky.textContent = map['3'].length + map['6'].length + map['9'].length;
        if (fam) fam.textContent = map['2'].length + map['5'].length + map['8'].length;
    });
}