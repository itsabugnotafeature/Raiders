from scripts import animations


class SpriteAnimator:

    def __init__(self, sprite):

        self.sprite = sprite

    def use(self, ability, animator):
        try:
            animator.set_animation(self.sprite, ability.animation)
        except AttributeError:
            print("ANIMATION: Failed to find animation for {}'s [{}] ability.".format(self.sprite.name, ability.name))
            print("ANIMATION: Reverting to default animation,")
            animator.set_animation(self.sprite, animations.attack())
