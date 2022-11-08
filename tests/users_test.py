import unittest
import unittest.mock
import users


def get_mock_db_cursor(fetchone_return_value=None, fetchall_return_value=None):
    return unittest.mock.Mock(
        __enter__=lambda _: unittest.mock.Mock(
            execute=lambda query, params: None,
            fetchone=lambda: fetchone_return_value,
            fetchall=lambda: fetchall_return_value,
        ),
        __exit__=lambda *args: None,
    )


def get_mock_db_connection(mock_db_cursor):
    return unittest.mock.Mock(
        __enter__=lambda _: unittest.mock.Mock(
            cursor=lambda **kwargs: mock_db_cursor,
        ),
        __exit__=lambda *args: None,
    )


class TestUserManagement(unittest.TestCase):

    def test_check_email_not_in_use_with_available_email(self):
        test_email = 'stc.3@b.com'
        mock_db_cursor = get_mock_db_cursor(fetchone_return_value=None)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            result = users.email_available(test_email)
            self.assertTrue(result)

    def test_check_email_not_in_use_with_unavailable_email(self):
        test_email = 'stc@b.com'
        mock_user_id = 1
        mock_db_cursor = get_mock_db_cursor(fetchone_return_value=mock_user_id)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            result = users.email_available(test_email)
            self.assertFalse(result)

    def test_check_user_with_credentials(self):
        test_email = 'rati.sudha86@gmail.com'
        test_password = 'rati1234'
        mock_user = {'id': 1, 'username': 'rati', 'email': test_email, 'hashed_password': b'$2b$12$AB0vaNyXNFr8REOZ8ZbgD.tHyYujj7tE/u1de6p9Mj5aspYBk.kmu'}
        mock_db_cursor = get_mock_db_cursor(fetchone_return_value=mock_user)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            result = users.get_user_with_credentials(test_email, test_password)
            self.assertEqual(result, mock_user)

    def test_check_login_details_with_user_by_id(self):
        username = 'rati'
        mock_db_cursor = get_mock_db_cursor(fetchone_return_value=None)
        mock_db_connection = get_mock_db_connection(mock_db_cursor)
        with unittest.mock.patch('mysql.connector.connect', return_value=mock_db_connection):
            result = users.get_user_by_id(username)
            self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()