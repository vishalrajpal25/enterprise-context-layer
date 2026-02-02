# ECP data access policy - allow by role and certification tier
package ecp.data_access

default allow = false

allow {
  input.action == "query"
  input.user.role != ""
  user_max_tier[input.user.role] >= input.data_product.certification_tier
}

user_max_tier := {
  "executive": 1,
  "finance_analyst": 2,
  "analyst": 3,
  "explorer": 4,
}
