document.addEventListener("DOMContentLoaded", function () {

    const recoveryForm = document.getElementById("recoveryForm");
    const submitButton = document.getElementById("submitButton");
    const formError = document.getElementById("formError");

    if (!recoveryForm) {
        console.error("Recovery form not found.");
        return;
    }

    recoveryForm.addEventListener("submit", async function (event) {

        event.preventDefault();

        formError.textContent = "";

        const transactionId =
            document.getElementById("transaction_id").value.trim();

        const amount =
            document.getElementById("amount").value;

        const transactionDate =
            document.getElementById("transaction_date").value;

        const issueType =
            document.getElementById("issue_type").value;

        const description =
            document.getElementById("description").value.trim();

        if (!transactionId || !amount || !issueType) {
            formError.textContent =
                "Please complete all required fields.";
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Analysing Transaction...";

        try {

            const response = await fetch("/api/analyze", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({

                    transaction_id: transactionId,
                    amount: amount,
                    transaction_date: transactionDate,
                    issue_type: issueType,
                    description: description

                })

            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(
                    result.error || "Transaction analysis failed."
                );
            }

            if (!result.case_id) {
                throw new Error("The server did not return a case ID.");
            }

            window.location.href = "/result/" + result.case_id;

        }

        catch (error) {

            console.error("Submission error:", error);

            formError.textContent =
                error.message || "Unable to process your request.";

            submitButton.disabled = false;
            submitButton.textContent = "Analyse My Transaction →";

        }

    });

});