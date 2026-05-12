class MLEngine:
    """
    Machine Learning Engine for Adaptive Lesson Recommendation
    """

    def __init__(self, weights=None):
        # 🔥 ruleWeights : Map (from UML)
        self.rule_weights = weights if weights else {
            "age": 0.3,
            "savings": 0.5,
            "behavior": 0.2
        }

        # 🔥 modelVersion : String (from UML)
        self.model_version = "v1.0"

    # ================= APPLY RULE MODEL =================
    def apply_rule_model(self, age, progress, behavior):
        """
        Wrapper method to apply rule-based scoring
        """
        return self.calculate_profile_score(age, progress, behavior)

    # ================= CALCULATE PROFILE SCORE =================
    def calculate_profile_score(self, age, progress, behavior):
        """
        Weighted scoring system
        """

        age_weight = age * self.rule_weights.get("age", 0.3)
        progress_weight = progress * self.rule_weights.get("savings", 0.5)
        behavior_weight = behavior * self.rule_weights.get("behavior", 0.2)

        return round(age_weight + progress_weight + behavior_weight, 2)

    # ================= SELECT PERSONALIZED LESSON =================
    def select_personalized_lesson(self, score, lessons):
        """
        Select lesson based on computed score
        """

        if not lessons:
            return None

        if score < 30:
            return lessons[0]

        elif score < 60:
            return lessons[min(1, len(lessons) - 1)]

        else:
            return lessons[min(2, len(lessons) - 1)]

    # 🔥 KEEP OLD METHOD NAME (BACKWARD COMPATIBILITY)
    def select_lesson(self, score, lessons):
        return self.select_personalized_lesson(score, lessons)

    # ================= TUNE MODEL =================
    def tune_model(self):
        """
        Simulated model tuning (admin-controlled optimization)
        """

        # Simple tuning logic (adjust weights slightly)
        self.rule_weights["age"] += 0.01
        self.rule_weights["savings"] -= 0.01

        return {
            "status": "Model tuning applied",
            "new_weights": self.rule_weights,
            "version": self.model_version
        }