
import { useEffect, useState } from "react";
import {
  getProfile,
  updateProfile,
  getSkills,
  addSkill,
  deleteSkill,
} from "../api/profile";
import { errorMessage } from "../utils/helpers";
import {
  Card,
  ErrorBox,
  SuccessBox,
  Spinner,
} from "../components/Ui";
import { Page } from "./Dashboard";

const empty = {
  full_name: "",
  phone: "",
  date_of_birth: "",
  college: "",
  degree: "",
  graduation_year: "",
  career_goal: "",
  bio: "",
};

const emptySkill = {
  name: "",
  proficiency: "beginner",
  years_of_experience: 0,
};

export default function Profile() {
  const [form, setForm] = useState(empty);

  const [skills, setSkills] = useState([]);

  const [skill, setSkill] =
    useState(emptySkill);

  const [loading, setLoading] =
    useState(true);

  const [saving, setSaving] =
    useState(false);

  const [skillSaving, setSkillSaving] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [error, setError] =
    useState("");

  const [skillMessage, setSkillMessage] =
    useState("");

  const [skillError, setSkillError] =
    useState("");

  const [deletingSkillId, setDeletingSkillId] =
    useState(null);


  /* =========================================================
     LOAD PROFILE
  ========================================================= */

  useEffect(() => {
    loadProfile();
  }, []);


  const loadProfile = async () => {
    try {
      const [profileData, skillsData] =
        await Promise.all([
          getProfile(),
          getSkills(),
        ]);

      setForm({
        ...empty,
        ...(profileData || {}),
      });

      setSkills(
        Array.isArray(skillsData)
          ? skillsData
          : skillsData?.skills ||
            skillsData?.results ||
            []
      );
    } catch (e) {
      setError(
        errorMessage(
          e,
          "Unable to load your profile."
        )
      );
    } finally {
      setLoading(false);
    }
  };


  /* =========================================================
     SAVE PROFILE
  ========================================================= */

  const submit = async (e) => {
    e.preventDefault();

    setSaving(true);
    setError("");
    setMessage("");

    try {
      await updateProfile(form);

      setMessage(
        "Profile saved successfully."
      );
    } catch (e) {
      setError(
        errorMessage(
          e,
          "Unable to save profile."
        )
      );
    } finally {
      setSaving(false);
    }
  };


  /* =========================================================
     ADD SKILL
  ========================================================= */

  const addNewSkill = async () => {
    setSkillError("");
    setSkillMessage("");

    const skillName =
      skill.name.trim();

    if (!skillName) {
      setSkillError(
        "Please enter a skill name."
      );
      return;
    }

    const duplicate = skills.some(
      (existingSkill) =>
        existingSkill.name
          ?.trim()
          .toLowerCase() ===
        skillName.toLowerCase()
    );

    if (duplicate) {
      setSkillError(
        "This skill is already in your profile."
      );
      return;
    }

    const years = Number(
      skill.years_of_experience
    );

    if (
      Number.isNaN(years) ||
      years < 0 ||
      years > 99
    ) {
      setSkillError(
        "Experience must be between 0 and 99 years."
      );
      return;
    }

    setSkillSaving(true);

    try {
      const data =
        await addSkill({
          name: skillName,
          proficiency:
            skill.proficiency,
          years_of_experience:
            years,
        });

      setSkills((prev) =>
        [...prev, data].sort(
          (a, b) =>
            (a.name || "").localeCompare(
              b.name || ""
            )
        )
      );

      setSkill(emptySkill);

      setSkillMessage(
        `${data.name} added to your skills.`
      );
    } catch (e) {
      setSkillError(
        errorMessage(
          e,
          "Unable to save skill."
        )
      );
    } finally {
      setSkillSaving(false);
    }
  };


  /* =========================================================
     DELETE SKILL
  ========================================================= */

  const removeSkill = async (
    skillItem
  ) => {
    if (!skillItem?.id) {
      setSkillError(
        "This skill cannot be removed because its ID is missing."
      );
      return;
    }

    const confirmed =
      window.confirm(
        `Remove "${skillItem.name}" from your profile?`
      );

    if (!confirmed) {
      return;
    }

    setSkillError("");
    setSkillMessage("");

    setDeletingSkillId(
      skillItem.id
    );

    try {
      await deleteSkill(
        skillItem.id
      );

      setSkills((prev) =>
        prev.filter(
          (item) =>
            item.id !==
            skillItem.id
        )
      );

      setSkillMessage(
        `${skillItem.name} removed from your profile.`
      );
    } catch (e) {
      setSkillError(
        errorMessage(
          e,
          "Unable to remove skill."
        )
      );
    } finally {
      setDeletingSkillId(null);
    }
  };


  /* =========================================================
     LOADING
  ========================================================= */

  if (loading) {
    return (
      <Page
        title="My Profile"
        subtitle="Loading your career profile…"
      >
        <div className="loading">
          <Spinner />
        </div>
      </Page>
    );
  }


  /* =========================================================
     UI
  ========================================================= */

  return (
    <Page
      title="My Profile"
      subtitle="Keep your career information accurate so CareerBridge can personalize its recommendations."
    >

      <div className="two-column">

        {/* ==================================================
            CAREER PROFILE
        ================================================== */}

        <Card
          title="Career profile"
          subtitle="Basic information used across your career journey."
        >

          <ErrorBox>
            {error}
          </ErrorBox>

          <SuccessBox>
            {message}
          </SuccessBox>

          <form
            className="form-grid"
            onSubmit={submit}
          >

            {[
              [
                "full_name",
                "Full name",
              ],
              [
                "phone",
                "Phone",
              ],
              [
                "college",
                "College / institution",
              ],
              [
                "degree",
                "Degree",
              ],
              [
                "graduation_year",
                "Graduation year",
              ],
              [
                "career_goal",
                "Target career",
              ],
            ].map(
              ([key, label]) => (
                <label key={key}>
                  {label}

                  <input
                    value={
                      form[key] || ""
                    }
                    onChange={(e) =>
                      setForm({
                        ...form,
                        [key]:
                          e.target.value,
                      })
                    }
                  />
                </label>
              )
            )}

            <label>
              Date of birth

              <input
                type="date"
                value={
                  form.date_of_birth ||
                  ""
                }
                onChange={(e) =>
                  setForm({
                    ...form,
                    date_of_birth:
                      e.target.value,
                  })
                }
              />
            </label>

            <label className="span-2">
              Bio

              <textarea
                rows="5"
                value={
                  form.bio || ""
                }
                onChange={(e) =>
                  setForm({
                    ...form,
                    bio:
                      e.target.value,
                  })
                }
              />
            </label>

            <div className="span-2">

              <button
                className="button primary"
                disabled={saving}
              >
                {saving
                  ? "Saving…"
                  : "Save profile"}
              </button>

            </div>

          </form>

        </Card>


        {/* ==================================================
            SKILLS
        ================================================== */}

        <Card
          title="Skills"
          subtitle="Add the skills you actually know so CareerBridge can use them for matching, skill-gap analysis, and career recommendations."
        >

          <div className="phase1-skills">

            <div className="phase1-skill-intro">

              <div>

                <strong>
                  Build your skill set
                </strong>

                <p>
                  Keep these skills
                  accurate. CareerBridge
                  uses them when comparing
                  your profile with job
                  descriptions.
                </p>

              </div>

              <div className="phase1-skill-count">

                <strong>
                  {skills.length}
                </strong>

                <span>
                  {skills.length === 1
                    ? "skill"
                    : "skills"}
                </span>

              </div>

            </div>


            <ErrorBox>
              {skillError}
            </ErrorBox>

            <SuccessBox>
              {skillMessage}
            </SuccessBox>


            {/* ADD SKILL */}

            <div className="phase1-skill-form">

              <div className="phase1-field">

                <label>
                  Skill name

                  <input
                    type="text"
                    placeholder="e.g. Python"
                    value={
                      skill.name
                    }
                    onChange={(e) =>
                      setSkill({
                        ...skill,
                        name:
                          e.target.value,
                      })
                    }
                    onKeyDown={(e) => {
                      if (
                        e.key ===
                        "Enter"
                      ) {
                        e.preventDefault();

                        addNewSkill();
                      }
                    }}
                  />

                </label>

              </div>


              <div className="phase1-field">

                <label>
                  Proficiency

                  <select
                    value={
                      skill.proficiency
                    }
                    onChange={(e) =>
                      setSkill({
                        ...skill,
                        proficiency:
                          e.target.value,
                      })
                    }
                  >

                    <option value="beginner">
                      Beginner
                    </option>

                    <option value="intermediate">
                      Intermediate
                    </option>

                    <option value="advanced">
                      Advanced
                    </option>

                  </select>

                </label>

              </div>


              <div className="phase1-field">

                <label>
                  Experience

                  <div className="phase1-experience-input">

                    <input
                      type="number"
                      min="0"
                      max="99"
                      step="0.1"
                      value={
                        skill.years_of_experience
                      }
                      onChange={(e) =>
                        setSkill({
                          ...skill,
                          years_of_experience:
                            e.target.value,
                        })
                      }
                    />

                    <span>
                      years
                    </span>

                  </div>

                </label>

              </div>


              <button
                type="button"
                className="button primary phase1-add-skill"
                onClick={
                  addNewSkill
                }
                disabled={
                  skillSaving
                }
              >
                {skillSaving
                  ? "Adding…"
                  : "+ Add skill"}
              </button>

            </div>


            {/* SKILL LIST */}

            <div className="phase1-skill-list-heading">

              <div>

                <strong>
                  Your skill set
                </strong>

                <span>
                  Skills currently saved
                  to your profile
                </span>

              </div>

            </div>


            {skills.length > 0 ? (

              <div className="phase1-skill-list">

                {skills.map(
                  (skillItem) => (

                    <div
                      className="phase1-skill-card"
                      key={
                        skillItem.id
                      }
                    >

                      <div className="phase1-skill-icon">
                        {(
                          skillItem.name ||
                          "S"
                        )
                          .charAt(0)
                          .toUpperCase()}
                      </div>


                      <div className="phase1-skill-details">

                        <strong>
                          {
                            skillItem.name
                          }
                        </strong>

                        <span>
                          {skillItem.proficiency
                            ?.charAt(0)
                            .toUpperCase() +
                            skillItem.proficiency?.slice(
                              1
                            )}

                          {" · "}

                          {
                            skillItem.years_of_experience
                          }

                          {" yrs experience"}
                        </span>

                      </div>


                      <button
                        type="button"
                        className="phase1-delete-skill"
                        title={`Remove ${skillItem.name}`}
                        aria-label={`Remove ${skillItem.name}`}
                        disabled={
                          deletingSkillId ===
                          skillItem.id
                        }
                        onClick={() =>
                          removeSkill(
                            skillItem
                          )
                        }
                      >
                        {deletingSkillId ===
                        skillItem.id
                          ? "…"
                          : "×"}
                      </button>

                    </div>

                  )
                )}

              </div>

            ) : (

              <div className="phase1-empty-skills">

                <div className="phase1-empty-icon">
                  +
                </div>

                <strong>
                  No skills added yet
                </strong>

                <p>
                  Add your first skill
                  above to make your
                  CareerBridge profile
                  more useful.
                </p>

              </div>

            )}

          </div>

        </Card>

      </div>

    </Page>
  );
}

