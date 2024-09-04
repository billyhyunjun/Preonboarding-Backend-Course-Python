# 게시판 작성 view 유닛 test 
회원 가입 및 로그인 기능, 게시글 작성 기능에 상황 테스트를 하여 알맞는 값이 나오는 지 테스트 해보았습니다.

## view 코드

### 회원 기능

```python
class AccountAPIView(APIView):
    # 회원 가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        
        if serializer.is_valid():
            username = serializer.validated_data['username']
            email = serializer.validated_data['email']
            
            
            # username중복 체크
            if User.objects.filter(username=username).exists():
                return Response({"error": "This name is already in use"}, status=status.HTTP_400_BAD_REQUEST)
            
            if email:
                if get_user_model().objects.filter(email=email).exists():
                    return Response({"Message": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class AccountDetailAPIView(APIView):
    # 로그인상태
    permission_classes = [IsAuthenticated]

    def get_user(self, user_id):
        return get_object_or_404(get_user_model(), pk=user_id)

    # 프로필 조회
    def get(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)
        # 2. serializer userdata
        serializer = UserDetailSerializer(user)
        # 3. return user using serializer
        return Response(serializer.data, status=200)

    # 비밀번호 변경
    def post(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)

        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # 3. get password_answer
        password_question = int(request.data.get("password_question"))
        password_answer = request.data.get("password_answer")
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        # 4. Verify with user data

        if password_question == user.password_question_id:
            if password_answer == user.password_answer:
                # 새로운 비밀번호와 확인용 비밀번호 일치 여부 확인
                if new_password != confirm_password:
                    return Response({"Error": "New password and confirm password do not match"}, status=status.HTTP_400_BAD_REQUEST)
                # save data
                user.set_password(new_password)  # 새로운 비밀번호 설정
                user.save()
                return Response({"Message": "password change successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"Message": "wrong password_answer"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Message": "wrong password_question"}, status=status.HTTP_400_BAD_REQUEST)

    # 프로필 수정
    def put(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)

        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # 3. Verify with data
        email = request.data.get("email")
        if email:
            if get_user_model().objects.filter(email=email).exists() and email != user.email:
                return Response({"Message": "email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user.email = email
        user.save()

        return Response({"Message": "User account update successfully"}, status=status.HTTP_200_OK)

    # 회원 탈퇴
    def delete(self, request, user_id):
        # 1. get user
        user = self.get_user(user_id)

        # 2. check if request user is the same as the user
        if request.user != user:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # 3. delete user account
        user.delete()
        return Response({"Message": "User account delete successfully"}, status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])  # POST입력만 받기
@permission_classes([IsAdminUser])  # 관리자 계정인지
def create_password(request):
    # 암호문 생성
    question = request.data.get("question")
    if not question:
        return Response({"error": "question is required"}, status=status.HTTP_400_BAD_REQUEST)

    question, _ = PasswordQuestion.objects.get_or_create(question=question)
    return Response({"id": question.id, "question": question.question}, status=status.HTTP_200_OK)
```

### 게시판

```python
class ArticleAPIView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # 게시물 전체 조회
    def get(self, request):
        tag = request.query_params.get("tag")
        search = request.query_params.get("search")
        sort = request.query_params.get("sort")

        articles = Article.objects.all()
        conditions = Q()
        
        if tag and search:
            if tag == "title":
                conditions &= Q(title__icontains=search)
            elif tag == "content":
                conditions &= Q(content__icontains=search)
            elif tag == "author":
                conditions &= Q(author__username__icontains=search)

        if conditions:
            articles = articles.filter(conditions)

        if sort:
            if sort == "likes":
                articles = articles.annotate(num_likes=Count('like_users')).order_by('-num_likes')
            elif sort == "views":
                articles = articles.annotate(num_views=Count('views')).order_by('-num_views')
            elif sort == "name":
                if tag == "title":
                    articles = articles.order_by('title')
                elif tag == "content":
                    articles = articles.order_by('content')
                elif tag == "author":
                    articles = articles.order_by('author')
            else:
                return Response({"error": "sort not matched"},
                                status=status.HTTP_400_BAD_REQUEST)

        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):

        # 클라이언트로부터 데이터 받기
        data = request.data

        # Serializer를 사용하여 유효성 검사 및 데이터 저장
        serializer = ArticleSerializer(data=data)

        # 필수 요소 확인
        required_fields = ["title", "url", "content"]
        if not all(field in data for field in required_fields):
            return Response({"error": "need required_fields(title, url, content)."}, status=status.HTTP_400_BAD_REQUEST)

        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)  # 현재 로그인한 사용자를 작성자로 저장
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticleDetailAPIView(APIView):
    
    def get_article(self, article_id):
        return get_object_or_404(Article, pk=article_id)

    # 게시물 상세 조회
    def get(self, request, article_id):
        
        article = self.get_article(article_id)

        user = request.user

        # 조회수 추가
        if not ArticleView.objects.filter(article=article, user=user).exists():
            # ArticleView에 조회 기록 추가
            ArticleView.objects.create(article=article, user=user)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시물 수정
    def put(self, request, article_id):

        # 게시물 존재 여부 확인
        article = self.get_article(article_id)

        # 프로필 유저와 로그인 유저가 일치하는지 확인
        if request.user != article.author:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        # 클라이언트로부터 데이터 받기
        data = request.data

        # Serializer를 사용하여 유효성 검사 및 데이터 수정
        serializer = ArticleSerializer(article, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):  
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    # 게시물 삭제
    def delete(self, request, article_id):

        # 게시물 존재 여부 확인
        article = self.get_article(article_id)

        # 프로필 유저와 로그인 유저가 일치하는지 확인
        if request.user != article.author:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        article.delete()
        return Response({"message": "article delete successfully"}, status=status.HTTP_204_NO_CONTENT)

    # 댓글 생성
    def post(self, request, article_id):
    
        article = self.get_article(article_id)

        content = request.data.get("content")

        if not content:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            content=content,
            article=article,
            author=request.user,
        )
        return Response({
            "id": comment.id,
            "article": comment.article.id,
            "author": comment.author.id,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)


class CommentAPIView(APIView):

    # 로그인상태
    permission_classes = [IsAuthenticated]

    def get_comment(self, comment_id):
        return get_object_or_404(Comment, pk=comment_id)

    # 대댓글 작성
    def post(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")

        if content is None:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment = Comment.objects.create(
            content=content,
            parent_comment=comment,
            author=request.user,
        )
        return Response({
            "id": comment.id,
            "parent_comment": comment.parent_comment.id,
            "author": comment.author.id,
            "content": comment.content,
        }, status=status.HTTP_201_CREATED)

    # 댓글 수정
    def put(self, request, comment_id):
        comment = self.get_comment(comment_id)
        content = request.data.get("content")

        if request.user != comment.author:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)
        
        if content is None:
            return Response({"error": "content is required"}, status=status.HTTP_400_BAD_REQUEST)

        comment.content = content
        comment.save()

        return Response({"Message": "comment updata successfully"}, status=status.HTTP_200_OK)

    # 댓글 삭제

    def delete(self, request, comment_id):

        comment = self.get_comment(comment_id)

        if request.user != comment.author:
            return Response({"error": "permission denied"}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()

        return Response({"Message": "comment delete successfully"}, status=status.HTTP_204_NO_CONTENT)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def like(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    user = request.user
    
    if article.like_users.filter(id=user.id).exists():
        article.like_users.remove(user.id)
        return Response({"Message": "The article like has been cancelled."}, status=status.HTTP_200_OK)
    else:
        article.like_users.add(user.id)
        return Response({"Message": "The article was liked."}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def favorite(request, article_id):
    article =  get_object_or_404(Article, id=article_id)
    user = request.user
    
    if article.favorites.filter(id=user.id).exists():
        article.favorites.remove(user.id)
        # 응답을 직렬화하고 반환
        return Response({"Message": "The article favorite has been cancelled."}, status=status.HTTP_200_OK)
    else:
        article.favorites.add(user.id)
        # 응답을 직렬화하고 반환
        return Response({"Message": "The article was favorite."}, status=status.HTTP_200_OK)
```

## 테스트

```python
User = get_user_model()  # 현재 활성화된 사용자 모델을 가져옵니다.


class AccountAPITest(TestCase):
    # 기본 셋팅
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin_user', email='admin@example.com', password='admin_password')

        # 암호 질문 생성
        self.password_question = PasswordQuestion.objects.create(
            question='What is your favorite color?')

        # 유저 생성
        self.user = User.objects.create_user(
            username='test_user', email='test@example.com', password='test_password', password_question_id=self.password_question.id, password_answer="Test Answer")

        # 모든 테스트에 사용할 사용자로 로그인
        self.client.force_authenticate(user=self.user)

    # 관리자로 로그인
    def test_create_password_question(self):
        self.client.force_authenticate(user=self.admin_user)

        # 유효한 질문을 포함하여 암호 질문 생성 (절대 경로로 수정)
        question_data = {'question': 'What is your favorite color?'}
        response = self.client.post('/api/accounts/password/', question_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 생성된 암호 질문이 데이터베이스에 있는지 확인
        created_question = PasswordQuestion.objects.get(
            question='What is your favorite color?')
        self.assertIsNotNone(created_question)

    # 비밀번호 변경 요청
    def test_change_password(self):
        change_data = {
            'password_question': self.password_question.id,
            'password_answer': 'Test Answer',
            'new_password': 'new_test_password',
            'confirm_password': 'new_test_password'
        }
        response = self.client.post(
            f'/api/accounts/profile/{self.user.id}/', change_data)

        # 변경 요청이 실패한 경우 오류 메시지 출력
        if response.status_code != status.HTTP_200_OK:
            print(response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 프로필 업데이트 요청
    def test_profile_update(self):
        update_data = {'email': 'new_email@example.com'}
        response = self.client.put(
            f'/api/accounts/profile/{self.user.id}/', update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 계정 삭제 요청
    def test_delete_account(self):
        response = self.client.delete(
            f'/api/accounts/profile/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
```

```python
class ArticleAPITest(TestCase):
    # 기본 셋팅
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    # 게시글 생성 테스트
    def test_create_article(self):
        url = reverse('articles:article')
        data = {
            'title': 'Test Article',
            'url': 'https://example.com',
            'content': 'This is a test article content.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # 게시글 비로그인 생성 테스트
    def test_create_article_unauthenticated(self):
        # Logout to make the user unauthenticated
        self.client.logout()  
        url = reverse('articles:article')
        data = {
            'title': 'Test Article',
            'url': 'https://example.com',
            'content': 'This is a test article content.'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # 게시글 필수요소 탈락 테스트
    def test_create_article_missing_fields(self):
        url = reverse('articles:article')
        data = {
            'title': 'Test Article',
            'content': 'This is a test article content.'
            # 'url' field is missing intentionally to test missing fields scenario
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # 게시글 전체 보기 테스트
    def test_get_articles(self):
        # First, create some articles
        Article.objects.create(
            title='Article 1', url='https://example.com/1', content='Content 1', author=self.user)
        Article.objects.create(
            title='Article 2', url='https://example.com/2', content='Content 2', author=self.user)

        url = reverse('articles:article')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # 게시글 필터링 테스트
    def test_get_articles_with_filtering(self):
        # First, create some articles
        Article.objects.create(
            title='Article with Tag', url='https://example.com/tag', content='Content 1', author=self.user)
        Article.objects.create(title='Article with Author',
                               url='https://example.com/author', content='Content 2', author=self.user)

        url = reverse('articles:article')
        response = self.client.get(url, {'tag': 'title', 'search': 'Author'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Article with Author')

    # 게시글 정렬 테스트
    def test_get_articles_with_sorting(self):
        # First, create some articles
        Article.objects.create(
            title='Article 1', url='https://example.com/1', content='Content 1', author=self.user)
        Article.objects.create(
            title='Article 2', url='https://example.com/2', content='Content 2', author=self.user)

        url = reverse('articles:article')
        response = self.client.get(url, {'sort': 'name'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Article 1')

    # 게시글 옳지않은 정렬 입력 테스트
    def test_get_articles_with_invalid_sorting(self):
        # First, create some articles
        Article.objects.create(
            title='Article 1', url='https://example.com/1', content='Content 1', author=self.user)

        url = reverse('articles:article')
        # Passing invalid sort parameter
        response = self.client.get(url, {'sort': 'invalid_sort'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


# ArticleDetailAPIViewTest 클래스를 정의합니다.
class ArticleDetailAPIViewTest(TestCase):
    # 테스트에 필요한 초기 상태를 설정합니다.
    def setUp(self):  # 각 테스트 메서드가 실행되기 전에 실행되는 설정 메서드입니다.
        self.user = User.objects.create_user(
            username='testuser', password='12345')  # testuser라는 이름의 사용자를 생성합니다.
        self.client = APIClient()  # API 클라이언트를 생성합니다.
        self.client.force_authenticate(user=self.user)  # 클라이언트를 특정 사용자로 인증합니다.
        self.article = Article.objects.create(  # Article 모델의 인스턴스를 생성하여 테스트할 게시물을 만듭니다.
            title='Test Article', content='Test Content', author=self.user)

    # 댓글 작성을 테스트하는 메서드입니다.
    def test_create_comment(self):
        url = reverse('articles:detail', kwargs={  # 'articles:detail' URL 패턴을 역으로 해석하여 URL을 생성합니다.
                      'article_id': self.article.id})

        data = {'content': 'Test Comment Content'}  # 댓글의 내용을 포함하는 데이터를 생성합니다.

        # 생성된 URL에 데이터를 전송하여 댓글을 작성합니다.
        response = self.client.post(url, data, format='json')
        # 응답의 상태 코드를 확인하여 요청이 성공적으로 처리되었는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        comment = Comment.objects.last()  # Comment 모델에서 마지막 댓글을 가져옵니다.
        # 작성된 내용과 게시물, 작성자가 올바른지 확인합니다.
        self.assertEqual(comment.content, 'Test Comment Content')
        self.assertEqual(comment.article, self.article)
        self.assertEqual(comment.author, self.user)

    # 댓글의 내용이 빠진 경우를 테스트하는 메서드입니다.
    def test_create_comment_missing_content(self):
        url = reverse('articles:detail', kwargs={  # 'articles:detail' URL 패턴을 역으로 해석하여 URL을 생성합니다.
                      'article_id': self.article.id})

        data = {}  # 데이터에 내용이 빠진 경우를 표현하기 위해 빈 딕셔너리를 생성합니다.

        # 생성된 URL에 데이터를 전송하여 댓글을 작성합니다.
        response = self.client.post(url, data, format='json')
        # 응답의 상태 코드를 확인하여 요청이 실패하고 '400 Bad Request' 상태 코드를 반환하는지 확인합니다.
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CommentAPIViewTest(TestCase):
    # 테스트를 위한 초기 설정
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345')  # 테스트용 유저 생성
        self.client = APIClient()  # 테스트용 클라이언트 생성
        self.client.force_authenticate(user=self.user)  # 인증된 유저로 설정
        self.article = Article.objects.create(
            title='Test Article', content='Test Content', author=self.user)  # 테스트용 게시물 생성
        self.comment = Comment.objects.create(
            content='Test Comment', author=self.user, article=self.article)  # 테스트용 댓글 생성

    # 답글 생성 테스트
    def test_create_reply(self):
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {'content': 'Test Reply Content'}  # 생성할 답글 데이터

        response = self.client.post(
            url, data, format='json')  # POST 요청하여 답글 생성

        self.assertEqual(response.status_code,
                         status.HTTP_201_CREATED)  # 응답 코드 확인
        reply = Comment.objects.last()  # 가장 최근에 생성된 댓글 가져오기
        self.assertEqual(reply.content, 'Test Reply Content')  # 답글 내용 확인
        self.assertEqual(reply.parent_comment, self.comment)  # 부모 댓글 확인
        self.assertEqual(reply.author, self.user)  # 작성자 확인

    # 댓글 생성 시 content가 없는 경우 테스트
    def test_create_reply_missing_content(self):
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {}  # content가 빠진 데이터

        response = self.client.post(
            url, data, format='json')  # POST 요청하여 답글 생성

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # 응답 코드 확인

    # 댓글 수정 테스트
    def test_update_comment(self):
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {'content': 'Updated Test Comment'}  # 수정할 댓글 데이터

        response = self.client.put(url, data, format='json')  # PUT 요청하여 댓글 수정

        self.assertEqual(response.status_code, status.HTTP_200_OK)  # 응답 코드 확인
        self.comment.refresh_from_db()  # DB에서 댓글 다시 가져오기
        self.assertEqual(self.comment.content,
                         'Updated Test Comment')  # 댓글 내용 확인

    # 댓글 수정 시 content가 없는 경우 테스트
    def test_update_missing_content(self):
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성
        data = {}  # content가 빠진 데이터

        response = self.client.put(url, data, format='json')  # PUT 요청하여 댓글 수정

        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)  # 응답 코드 확인

    # 댓글 삭제 테스트
    def test_delete_comment(self):
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성

        response = self.client.delete(url)  # DELETE 요청하여 댓글 삭제

        self.assertEqual(response.status_code,
                         status.HTTP_204_NO_CONTENT)  # 응답 코드 확인
        self.assertFalse(Comment.objects.filter(
            pk=self.comment.id).exists())  # 댓글이 삭제되었는지 확인

    # 다른 유저가 댓글 삭제 시도 시 테스트
    def test_delete_comment_wrong_user(self):
        another_user = User.objects.create_user(
            username='anotheruser', password='12345')  # 다른 유저 생성
        self.client.force_authenticate(user=another_user)  # 다른 유저로 인증 설정
        url = reverse('articles:comment', kwargs={
                      'comment_id': self.comment.id})  # URL 생성

        response = self.client.delete(url)  # DELETE 요청하여 댓글 삭제

        self.assertEqual(response.status_code,
                         status.HTTP_403_FORBIDDEN)  # 응답 코드 확인


class ArticleLikeAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)
        self.article = Article.objects.create(
            title='Test Article', content='Test Content', author=self.user)

    def test_like_article(self):
        url = reverse('articles:like', kwargs={'article_id': self.article.id})
        response = self.client.post(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Message'], 'The article was liked.')

    def test_cancel_like_article(self):
        # First, like the article
        self.article.like_users.add(self.user)

        url = reverse('articles:like', kwargs={'article_id': self.article.id})
        response = self.client.post(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Message'],
                         'The article like has been cancelled.')

    def test_favorite_article(self):
        url = reverse('articles:favorite', kwargs={'article_id': self.article.id})
        response = self.client.post(url)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Message'], 'The article was favorite.')

    def test_cancel_favorite_article(self):
        # First, favorite the article
        self.article.favorites.add(self.user)

        url = reverse('articles:favorite', kwargs={'article_id': self.article.id})
        response = self.client.post(url) 
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Message'],
                         'The article favorite has been cancelled.')
```

## 테스트 결과

![image](https://github.com/user-attachments/assets/e04fcc14-4cf2-4cb3-9cc9-c8212831d199)
