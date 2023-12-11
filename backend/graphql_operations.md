# Test the queries and mutations below

query Query {
  get_users {
    ... on UsersSuccess {
      users {
        id
        firstname
        lastname
        username
        role
        birthdate
      }
    }

    ... on GraphqlError {
      custom_error
    }
  }
}

mutation Mutation($login_input: login_input!) {
  login_user(login_input: { username: "@Mark", password: "TEST" }) {
    ... on UserResponse {
      user {
        id
        firstname
        lastname
        role
        birthdate
      }
      access_token
    }
    ... on GraphqlError {
      custom_error
    }
  }
}

mutation Mutation($create_user_input: create_user_input!) {
  create_user(
    create_user_input: {
      firstname: "Attila"
      lastname: "Kaiid"
      username: "@At"
      password: "TEST"
      role: ADMIN
      birthdate: "1980-11-30"
    }
  ) {
    ... on Success {
      message
    }
    ... on GraphqlError {
      custom_error
    }
  }
}

mutation Delete_user($deleteUserId: ID!) {
  delete_user(id: "clq13q2y4000185wguqvrlu5r") {
    ... on Success {
      message
    }
    ... on GraphqlError {
      custom_error
    }
  }
}

query Search_user($username: String!) {
  search_user(username: "@At") {
    ... on User {
      id
      firstname
      lastname
      username
      role
      password
      birthdate
    }
    ... on GraphqlError {
      custom_error
    }
  }
}

mutation Update_user($updateUserId: ID!, $updateUserInput: update_user_input!) {
  update_user(
    id: "clq00gtgd0000853o9epn4hwb"
    update_user_input: {
      new_username: "@Roli"
      new_firstname: "Roland"
      new_role: ADMIN
    }
  ) {
    ... on Success {
      message
    }
    ... on GraphqlError {
      custom_error
    }
  }
}



query Query {
  logout_user
}
