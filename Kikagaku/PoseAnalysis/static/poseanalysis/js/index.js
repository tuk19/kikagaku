function showLoading() {
    let errorMsg = document.getElementById("error_message");
    let fpsRate = document.getElementById('fps_rate');
    let video_file = document.getElementById('id_video_file');
    let loading_message =  document.getElementById('loading_message')

    if (errorMsg) {
        errorMsg.innerText = '';
    }

    // if (fpsRate !== '1') {
    //     fpsRate.value = '1';
    // }

    // if (video_file) {
    //     video_file.value = '';
    // }

    loading_message.style.display = 'block';
    loading_message.style.color = 'red';
}


// document.getElementById("poseForm").addEventListener("submit", async function (e) {
//     e.preventDefault();

//     const form = e.target;
//     const formData = new FormData(form);
//     const downloadUrl = "{% url 'poseanalysis:index' %}";

//     // 処理中メッセージ表示
//     document.getElementById("loading_message").style.display = "block";

//     try {
//         const response = await fetch(downloadUrl, {
//             method: "POST",
//             headers: {
//                 "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
//             },
//             body: formData,
//         });

//         if (!response.ok) throw new Error("ダウンロード失敗");

//         const blob = await response.blob();
//         const url = URL.createObjectURL(blob);

//         // 自動ダウンロード
//         const a = document.createElement("a");
//         a.href = url;
//         a.download = "pose_result.mp4";
//         a.click();

//       // URL オブジェクトを解放
//         URL.revokeObjectURL(url);

//     } catch (error) {
//         alert("エラーが発生しました: " + error.message);
//     } finally {
//       // 処理中メッセージを非表示に
//         document.getElementById("loading_message").style.display = "none";
//     }
// });
