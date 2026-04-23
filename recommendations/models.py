from django.db import models


class FitnessRecord(models.Model):
    """Stores each fitness recommendation for progress tracking."""

    # User input fields
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    height = models.FloatField(help_text="Height in cm")
    weight = models.FloatField(help_text="Weight in kg")
    bmi = models.FloatField()
    goal = models.CharField(max_length=30)
    activity_level = models.CharField(max_length=20)
    experience_level = models.CharField(max_length=20)

    # ML prediction results
    workout = models.CharField(max_length=50)
    diet = models.CharField(max_length=50)

    # Tracking metadata
    session_key = models.CharField(max_length=100, db_index=True,
                                   help_text="Browser session ID for tracking")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.gender}, age {self.age}, {self.goal} — {self.created_at:%Y-%m-%d %H:%M}"
