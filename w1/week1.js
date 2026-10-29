"use strict";

document.querySelectorAll("[data-check-quiz]").forEach((button) => {
  const quiz = button.closest("[data-quiz]");
  const questions = [...quiz.querySelectorAll(".quiz-question")];

  quiz.querySelectorAll("input").forEach((input) => {
    input.addEventListener("change", () => {
      const question = input.closest(".quiz-question");
      question.dataset.state = "";
      const feedback = question.querySelector(".question-feedback");
      feedback.textContent = "";
      feedback.dataset.state = "";
      quiz.querySelector("[data-quiz-status]").textContent = "Answer updated. Check again for feedback.";
    });
  });

  button.addEventListener("click", () => {
    let answered = 0;
    let correct = 0;

    questions.forEach((question) => {
      const choice = question.querySelector("input:checked");
      const feedback = question.querySelector(".question-feedback");
      question.dataset.state = "";

      if (!choice) {
        feedback.textContent = "Choose one answer, then check again.";
        feedback.dataset.state = "";
        return;
      }

      answered += 1;
      const isCorrect = choice.dataset.correct === "true";
      if (isCorrect) correct += 1;
      question.dataset.state = isCorrect ? "correct" : "incorrect";
      feedback.dataset.state = isCorrect ? "correct" : "incorrect";
      feedback.textContent = isCorrect
        ? `That’s right. ${question.dataset.explanation}`
        : `Not quite. ${question.dataset.explanation}`;
    });

    const status = quiz.querySelector("[data-quiz-status]");
    if (answered < questions.length) {
      status.textContent = `Answer all ${questions.length} questions to see your check: ${answered} answered so far.`;
    } else {
      status.textContent = correct === questions.length
        ? `All ${questions.length} answers fit. Explain one answer to a partner, then continue to the lab.`
        : `${correct} of ${questions.length} answers fit. Read the explanations, change any answer, and check again.`;
    }
    const missing = questions.find((question) => !question.querySelector("input:checked"));
    if (missing) missing.querySelector("input").focus();
  });

  quiz.querySelector("[data-reset-quiz]").addEventListener("click", () => {
    quiz.querySelectorAll("input").forEach((input) => { input.checked = false; });
    questions.forEach((question) => {
      question.dataset.state = "";
      const feedback = question.querySelector(".question-feedback");
      feedback.textContent = "";
      feedback.dataset.state = "";
    });
    quiz.querySelector("[data-quiz-status]").textContent = "Answers cleared. Start again whenever you are ready.";
    questions[0].querySelector("input").focus();
  });
});

document.querySelectorAll("[data-check-matches]").forEach((button) => {
  const activity = button.closest("[data-matching-activity]");
  const cards = [...activity.querySelectorAll("[data-scenario]")];
  const status = activity.querySelector("[data-match-status]");

  button.addEventListener("click", () => {
    const unanswered = cards.filter((card) => !card.querySelector("select").value);
    if (unanswered.length) {
      status.textContent = `Choose an approach for all ${cards.length} situations. ${unanswered.length} ${unanswered.length === 1 ? "answer is" : "answers are"} still missing.`;
      unanswered[0].querySelector("select").focus();
      return;
    }

    const attempt = Number(activity.dataset.attempts || "0") + 1;
    activity.dataset.attempts = String(attempt);
    let correct = 0;

    cards.forEach((card) => {
      const select = card.querySelector("select");
      const feedback = card.querySelector(".scenario-feedback");
      const isCorrect = select.value === card.dataset.answer;
      card.dataset.state = isCorrect ? "correct" : "review";

      if (isCorrect) {
        correct += 1;
        feedback.textContent = `Good fit. ${card.dataset.rationale}`;
      } else if (attempt >= 2) {
        feedback.textContent = `Best fit: ${card.dataset.answerLabel}. ${card.dataset.rationale}`;
      } else {
        feedback.textContent = `Try once more. Hint: ${card.dataset.hint}`;
      }
    });

    if (correct === cards.length) {
      status.textContent = `All ${cards.length} matches fit. Be ready to explain the clues you used.`;
    } else if (attempt >= 2) {
      status.textContent = `${correct} of ${cards.length} fit your choices. The best fit and its reason are now shown for each situation.`;
    } else {
      status.textContent = `${correct} of ${cards.length} fit so far. Revisit the hints, change any choice, and check again.`;
    }
  });

  activity.querySelectorAll("select").forEach((select) => {
    select.addEventListener("change", () => {
      const card = select.closest("[data-scenario]");
      card.dataset.state = "";
      card.querySelector(".scenario-feedback").textContent = "";
      status.textContent = "Choice updated. Check your matches to see feedback.";
    });
  });

  activity.querySelector("[data-reset-matches]").addEventListener("click", () => {
    cards.forEach((card) => {
      card.querySelector("select").value = "";
      card.querySelector(".scenario-feedback").textContent = "";
      card.dataset.state = "";
    });
    activity.dataset.attempts = "0";
    status.textContent = "Choices cleared. Start again whenever you are ready.";
    cards[0].querySelector("select").focus();
  });
});

// Include worked examples and the answer key when the teacher prints a page.
// Restore the original disclosure state after printing.
let printDetails = [];
window.addEventListener("beforeprint", () => {
  if (printDetails.length) return;
  printDetails = [...document.querySelectorAll("details")].map((details) => ({ details, open: details.open }));
  printDetails.forEach(({ details }) => { details.open = true; });
});
window.addEventListener("afterprint", () => {
  printDetails.forEach(({ details, open }) => { details.open = open; });
  printDetails = [];
});
