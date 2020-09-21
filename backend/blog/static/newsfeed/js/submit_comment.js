function submitComment(event,$form) {
    event.preventDefault();
    parentType = $form.attr('data-parent-type')
    parentId = $form.attr('data-parent-id')
    console.log(parentId)
    console.log(parentType)
    commentContent = $form.find("#main_comment_form").val();
    $.ajax({
        type: 'POST',
        url: '../new_comment/',
        data: {
            parentType: parentType,
            parentId: parentId,
            commentContent: commentContent,
            csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val()
        }
    })
}

$('#main_form').on('submit',function(e){
    submitComment(e,$(this))
})