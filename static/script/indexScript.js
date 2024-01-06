async function methodInput() {
    const method = document.getElementById('method').value;
    var container = document.getElementById('parameterContainer');

    if (method == "1") {
        container.innerHTML = '<form action="/method1" method="post" enctype="multipart/form-data"><label for="T">จำนวนต้นไม้ในพื้นที่โครงการทั้งหมด (ต้น): </label><input type="number" id="T" name="T"><label for="t">ปีที่ดำเนินการติดตามผล (ปี) : </label><input type="number" id="t" name="t"><label for="MAI"> อัตราการเพิ่มพูนปริมาณการกักเก็บคาร์บอนของต้นไม้ (kgCO2/ต้น/ปี): </label><input type="number" id="MAI" name="MAI"><br><input class="calculateButton" type="submit" value="Calculate"></form>';
    }

    if (method == "2") {
        container.innerHTML = '<h1>Upload CSV/ Excel File</h1><form action="/method2" method="post" enctype="multipart/form-data"><input type="file" name="file"><input class="uploadButton" type="submit" value="Upload"></form>';
    }
}

// async function calculateCTT() {
//     const method = document.getElementById('method').value;
//     var CTT = document.getElementById("CTT_default");

//     if (method == "1") {
//         const t = document.getElementById('t').value;
//         const T = document.getElementById('T').value;
//         const MAI = document.getElementById('MAI').value;

//         CTT.textContent = "CTT: " + (t * T * MAI * 0.001).toString();
//     }

//     else {
//         CTT.textContent = "";
//     }
// }