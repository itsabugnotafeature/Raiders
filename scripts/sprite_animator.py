from scripts import animations


class SpriteAnimator:

    def __init__(self, sprite):

        self.sprite = sprite

    def use(self, ability, outcome, animator):

        # TODO: give each ability an AnimationPack, but also give every sprite a default s/f/p AnimationPack
        try:
            if outcome["blocked"]:
                print("ANIMATION: Attempted to play blocked animation for {}.".format(self.sprite))
                animator.set_animation(self.sprite, ability.blocked_animation)
            elif outcome["blocking"]:
                print("ANIMATION: Attempted to play blocking animation for {}.".format(self.sprite))
                animator.set_animation(self.sprite, ability.blocking_animation)
            else:
                animator.set_animation(self.sprite, ability.animation)
        except AttributeError:
            print("ANIMATION: Failed to find animation for {}'s {} ability.".format(self.sprite.name, ability))
            print("ANIMATION: Reverting to default animation,")
            animator.set_animation(self.sprite, animations.attack())
